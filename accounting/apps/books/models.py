from decimal import Decimal as D
from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation)
from django.contrib.contenttypes.models import ContentType

from accounting.libs import prices
from accounting.libs.templatetags.currency_filters import currency_formatter
from .managers import InvoiceQuerySet, BillQuerySet
from .utils import next_invoice_number


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

    class Meta:
        pass

    def __str__(self):
        return self.name

    @property
    def rate(self):
        r = D('0.000')
        for c in self.components.all():
            r += c.percentage
        return r


class TaxComponent(models.Model):
    """
    See the `TaxRate` class for an explanation
    """
    tax_rate = models.ForeignKey('books.TaxRate',
                                 related_name="components")

    name = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=6,
                                     decimal_places=5,
                                     validators=[MinValueValidator(D('0')),
                                                 MaxValueValidator(D('1'))])


class AbstractInvoice(models.Model):
    number = models.CharField(max_length=6,
                              default=next_invoice_number)

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
    draft = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    date_issued = models.DateField(default=date.today)
    date_dued = models.DateField()
    date_paid = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "#{} ({})".format(self.number, self.total_incl_tax)

    def compute_totals(self):
        self.total_excl_tax = self.get_total_excl_tax()
        self.total_incl_tax = self.get_total_incl_tax()

    def _get_total(self, prop):
        """
        For executing a named method on each line of the basket
        and returning the total.
        """
        total = D('0.00')
        for line in self.lines.all():
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
        return self.payments.all().aggregate(sum=Sum('amount'))["sum"]

    @property
    def total_due_incl_tax(self):
        due = self.total_incl_tax
        due -= self.total_paid
        return due


class AbstractInvoiceLine(models.Model):
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
        tax = unit * settings.ACCOUNTING_DEFAULT_TAX_PERCENTAGE
        p = prices.Price(settings.ACCOUNTING_DEFAULT_CURRENCY, unit, tax=tax)
        return p

    @property
    def line_price_excl_tax(self):
        return self.quantity * self.unit_price.excl_tax

    @property
    def line_price_incl_tax(self):
        return self.quantity * self.unit_price.incl_tax

    def from_client(self):
        raise NotImplementedError

    def to_client(self):
        raise NotImplementedError


class Invoice(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     related_name="invoices",
                                     verbose_name="From Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="To Client")
    payments = GenericRelation('books.Payment')

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-date_issued', 'id')

    def from_client(self):
        return self.organization

    def to_client(self):
        return self.client


class InvoiceLine(AbstractInvoiceLine):
    invoice = models.ForeignKey('books.Invoice',
                                related_name="lines")
    tax_rate = models.ForeignKey('books.TaxRate')

    class Meta:
        pass


class Bill(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     related_name="bills",
                                     verbose_name="To Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="From Client")
    payments = GenericRelation('books.Payment')

    objects = BillQuerySet.as_manager()

    class Meta:
        unique_together = (("number", "organization"),)
        ordering = ('-date_issued', 'id')

    def from_client(self):
        return self.client

    def to_client(self):
        return self.organization


class BillLine(AbstractInvoiceLine):
    bill = models.ForeignKey('books.Bill',
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
