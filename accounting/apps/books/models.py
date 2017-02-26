from decimal import Decimal as D
from datetime import date

from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation)
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from accounting.libs import prices
from accounting.libs.checks import CheckingModelMixin
from accounting.libs.templatetags.currency_filters import currency_formatter
from accounting.libs.templatetags.format_filters import percentage_formatter
from .managers import (
    EstimateQuerySet,
    InvoiceQuerySet,
    BillQuerySet,
    ExpenseClaimQuerySet)

TWO_PLACES = D(10) ** -2


class Organization(models.Model):
    display_name = models.CharField(max_length=150,
        help_text="Name that you communicate")
    legal_name = models.CharField(max_length=150,
        help_text="Official name to appear on your reports, sales "
                  "invoices and bills")

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name="owned_organizations")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name="organizations",
                                     blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.legal_name

    def get_absolute_url(self):
        return reverse('books:organization-detail', args=[self.pk])

    @property
    def turnover_excl_tax(self):
        return self.invoices.turnover_excl_tax() or D('0.00')

    @property
    def turnover_incl_tax(self):
        return self.invoices.turnover_incl_tax() or D('0.00')

    @property
    def debts_excl_tax(self):
        return self.bills.debts_excl_tax() or D('0.00')

    @property
    def debts_incl_tax(self):
        return self.bills.debts_incl_tax() or D('0.00')

    @property
    def profits(self):
        return self.turnover_excl_tax - self.debts_excl_tax

    @property
    def collected_tax(self):
        return self.turnover_incl_tax - self.turnover_excl_tax

    @property
    def deductible_tax(self):
        return self.debts_incl_tax - self.debts_excl_tax

    @property
    def tax_provisionning(self):
        return self.collected_tax - self.deductible_tax

    @property
    def overdue_total(self):
        due_invoices = self.invoices.dued()
        due_turnonver = due_invoices.turnover_incl_tax()
        total_paid = due_invoices.total_paid()
        return due_turnonver - total_paid


class TaxRate(models.Model):
    """
    Every transaction line item needs a Tax Rate.
    Tax Rates can have multiple Tax Components.

    For instance, you can have an item that is charged a Tax Rate
    called "City Import Tax (8%)" that has two components:
        - a city tax of 5%
        - an import tax of 3%.

    *inspired by Xero*
    """
    organization = models.ForeignKey('books.Organization',
                                     related_name="tax_rates",
                                     verbose_name="Attached to Organization")

    name = models.CharField(max_length=50)
    rate = models.DecimalField(max_digits=6,
                               decimal_places=5,
                               validators=[MinValueValidator(D('0')),
                                           MaxValueValidator(D('1'))])

    class Meta:
        pass

    def __str__(self):
        return "{} ({})".format(self.name, percentage_formatter(self.rate))


class AbstractSale(CheckingModelMixin, models.Model):
    number = models.IntegerField(default=1,
                                 db_index=True)

    # Total price needs to be stored with and wihtout taxes
    # because the tax percentage can vary depending on the associated lines
    total_incl_tax = models.DecimalField("Total (inc. tax)",
                                         decimal_places=2,
                                         max_digits=12,
                                         default=D('0'))
    total_excl_tax = models.DecimalField("Total (excl. tax)",
                                         decimal_places=2,
                                         max_digits=12,
                                         default=D('0'))

    # tracking
    date_issued = models.DateField(default=date.today)
    date_dued = models.DateField("Due date",
                                 blank=True, null=True,
                                 help_text="The date when the total amount "
                                           "should have been collected")
    date_paid = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    class CheckingOptions:
        fields = (
            'total_incl_tax',
            'total_excl_tax',
            'date_dued',
        )

    def __str__(self):
        return "#{} ({})".format(self.number, self.total_incl_tax)

    def get_detail_url(self):
        raise NotImplementedError

    def get_edit_url(self):
        raise NotImplementedError

    def compute_totals(self):
        self.total_excl_tax = self.get_total_excl_tax()
        self.total_incl_tax = self.get_total_incl_tax()

    def _get_total(self, prop):
        """
        For executing a named method on each line of the basket
        and returning the total.
        """
        total = D('0.00')
        line_queryset = self.lines.all()
        for line in line_queryset:
            total = total + getattr(line, prop)
        return total

    @property
    def total_tax(self):
        return self.total_incl_tax - self.total_excl_tax

    def get_total_excl_tax(self):
        return self._get_total('line_price_excl_tax')

    def get_total_incl_tax(self):
        return self._get_total('line_price_incl_tax')

    @property
    def total_paid(self):
        total = D('0')
        for p in self.payments.all():
            total += p.amount
        return total

    @property
    def total_due_incl_tax(self):
        due = self.total_incl_tax
        due -= self.total_paid
        return due

    def is_fully_paid(self):
        paid = self.total_paid.quantize(TWO_PLACES)
        total = self.total_incl_tax.quantize(TWO_PLACES)
        return paid >= total

    def is_partially_paid(self):
        paid = self.total_paid.quantize(TWO_PLACES)
        total = self.total_incl_tax.quantize(TWO_PLACES)
        return paid and paid > 0 and paid < total

    @property
    def payroll_taxes(self):
        # TODO implement collected/accurial
        paid = self.total_paid
        payroll = D('0')
        for emp in self.organization.employees.all():
            if not emp.salary_follows_profits:
                continue
            payroll += paid * emp.shares_percentage * emp.payroll_tax_rate
        return payroll

    def _check_total(self, check, total, computed_total):
        if total.quantize(TWO_PLACES) != computed_total.quantize(TWO_PLACES):
            check.mark_fail(level=check.LEVEL_ERROR,
                            message="The computed amount isn't correct, it "
                                    "should be {}, please edit and save the "
                                    "{} to fix it.".format(
                                        currency_formatter(total),
                                        self._meta.verbose_name))
        else:
            check.mark_pass()
        return check

    def check_total_excl_tax(self, check):
        total = self.get_total_excl_tax()
        return self._check_total(check, total, self.total_excl_tax)

    def check_total_incl_tax(self, check):
        total = self.get_total_incl_tax()
        return self._check_total(check, total, self.total_incl_tax)

    def check_date_dued(self, check):
        if self.date_dued is None:
            check.mark_fail(message="No due date specified")
            return check

        if self.total_excl_tax == D('0'):
            check.mark_fail(message="The invoice has no value")
            return check

        if self.is_fully_paid():
            last_payment = self.payments.all().first()
            formatted_date = last_payment.date_paid.strftime('%B %d, %Y')
            check.mark_pass(message="Has been paid on the {}"
                .format(formatted_date))
            return check

        if timezone.now().date() > self.date_dued:
            check.mark_fail(message="The due date has been exceeded.")
        else:
            check.mark_pass()
        return check


class AbstractSaleLine(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit_price_excl_tax = models.DecimalField(max_digits=8,
                                              decimal_places=2)
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2,
                                   default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    @property
    def unit_price(self):
        """Returns the `Price` instance representing the instance"""
        unit = self.unit_price_excl_tax
        tax = unit * self.tax_rate.rate
        p = prices.Price(settings.ACCOUNTING_DEFAULT_CURRENCY, unit, tax=tax)
        return p

    @property
    def line_price_excl_tax(self):
        return self.quantity * self.unit_price.excl_tax

    @property
    def line_price_incl_tax(self):
        return self.quantity * self.unit_price.incl_tax

    @property
    def taxes(self):
        return self.line_price_incl_tax - self.line_price_excl_tax

    def from_client(self):
        raise NotImplementedError

    def to_client(self):
        raise NotImplementedError


class Estimate(AbstractSale):
    organization = models.ForeignKey('books.Organization',
                                     related_name="estimates",
                                     verbose_name="From Organization")
    client = models.ForeignKey('people.Client',
                               verbose_name="To Client")

    objects = EstimateQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-number',)

    def get_detail_url(self):
        return reverse('books:estimate-detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('books:estimate-edit', args=[self.pk])

    def from_client(self):
        return self.organization

    def to_client(self):
        return self.client


class EstimateLine(AbstractSaleLine):
    invoice = models.ForeignKey('books.Estimate',
                                related_name="lines")
    tax_rate = models.ForeignKey('books.TaxRate')

    class Meta:
        pass


class Invoice(AbstractSale):
    organization = models.ForeignKey('books.Organization',
                                     related_name="invoices",
                                     verbose_name="From Organization")
    client = models.ForeignKey('people.Client',
                               verbose_name="To Client")
    payments = GenericRelation('books.Payment')

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-number',)

    def get_detail_url(self):
        return reverse('books:invoice-detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('books:invoice-edit', args=[self.pk])

    def from_client(self):
        return self.organization

    def to_client(self):
        return self.client


class InvoiceLine(AbstractSaleLine):
    invoice = models.ForeignKey('books.Invoice',
                                related_name="lines")
    tax_rate = models.ForeignKey('books.TaxRate')

    class Meta:
        pass


class Bill(AbstractSale):
    organization = models.ForeignKey('books.Organization',
                                     related_name="bills",
                                     verbose_name="To Organization")
    client = models.ForeignKey('people.Client',
                               verbose_name="From Client")
    payments = GenericRelation('books.Payment')

    objects = BillQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-number',)

    def get_detail_url(self):
        return reverse('books:bill-detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('books:bill-edit', args=[self.pk])

    def from_client(self):
        return self.client

    def to_client(self):
        return self.organization


class BillLine(AbstractSaleLine):
    bill = models.ForeignKey('books.Bill',
                             related_name="lines")
    tax_rate = models.ForeignKey('books.TaxRate')

    class Meta:
        pass


class ExpenseClaim(AbstractSale):
    organization = models.ForeignKey('books.Organization',
                                     related_name="expense_claims",
                                     verbose_name="From Organization")
    employee = models.ForeignKey('people.Employee',
                                 verbose_name="Paid by employee")
    payments = GenericRelation('books.Payment')

    objects = ExpenseClaimQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-number',)

    def get_detail_url(self):
        return reverse('books:expense_claim-detail', args=[self.pk])

    def get_edit_url(self):
        return reverse('books:expense_claim-edit', args=[self.pk])

    def from_client(self):
        return self.employee

    def to_client(self):
        return self.organization


class ExpenseClaimLine(AbstractSaleLine):
    expense_claim = models.ForeignKey('books.ExpenseClaim',
                                      related_name="lines")
    tax_rate = models.ForeignKey('books.TaxRate')

    class Meta:
        pass


class Payment(models.Model):
    amount = models.DecimalField("Amount",
                                 decimal_places=2,
                                 max_digits=12)
    detail = models.CharField(max_length=255,
                              blank=True,
                              null=True)
    date_paid = models.DateField(default=date.today)
    reference = models.CharField(max_length=255,
                                 blank=True,
                                 null=True)

    # relationship to an object
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-date_paid',)

    def __str__(self):
        if self.detail:
            return self.detail
        return "Payment of {}".format(currency_formatter(self.amount))
