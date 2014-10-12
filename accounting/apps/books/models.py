from decimal import Decimal, ROUND_HALF_EVEN
from datetime import date

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import AbstractUser, UserManager

from libs.utils import banker_round
from libs import prices
from .managers import InvoiceQuerySet, BillQuerySet
from .utils import next_invoice_number


class User(AbstractUser):
    objects = UserManager()


class Organization(models.Model):
    display_name = models.CharField(max_length=150,
        help_text="Name that you communicate")
    legal_name = models.CharField(max_length=150,
        help_text="Official name to appear on your reports, sales "
                  "invoices and bills")

    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name="organizations",
                                     blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.legal_name

    @property
    def turnover(self):
        return self.invoices.turnover()

    @property
    def debts(self):
        return self.bills.debts()

    @property
    def profit(self):
        return self.turnover - self.debts


class AbstractInvoice(models.Model):
    number = models.CharField(max_length=6,
                              unique=True,
                              default=next_invoice_number)

    # Total price needs to be stored with and wihtout taxes
    # because the tax percentage can vary depending on the associated lines
    total_incl_tax = models.DecimalField("Total (inc. tax)",
                                         decimal_places=2,
                                         max_digits=12)
    total_excl_tax = models.DecimalField("Total (excl. tax)",
                                         decimal_places=2,
                                         max_digits=12)

    # tracking
    draft = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    date_issued = models.DateField(default=date.today)
    date_paid = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "#{} ({})".format(self.number, self.total())

    def save(self, *args, **kwargs):
        # recompute total_incl_tax and total_excl_tax
        self.total_excl_tax = self.get_total_excl_tax()
        self.total_incl_tax = self.get_total_incl_tax()
        super().save(*args, **kwargs)

    def _get_total(self, prop):
        """
        For executing a named method on each line of the basket
        and returning the total.
        """
        total = Decimal('0.00')
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
        tax = unit * settings.DEFAULT_TAX_PERCENTAGE
        return prices.Price(settings.DEFAULT_CURRENCY, unit, tax=tax)

    @property
    def line_price_excl_tax(self):
        return self.quantity * self.unit_price.excl_tax

    @property
    def line_price_incl_tax(self):
        return self.quantity * self.unit_price.incl_tax


class Invoice(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     related_name="invoices",
                                     verbose_name="From Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="To Client")

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        ordering = ('-date_issued', 'id')


class InvoiceLine(AbstractInvoiceLine):
    invoice = models.ForeignKey('books.Invoice',
                                related_name="lines")

    class Meta:
        pass


class Bill(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     related_name="bills",
                                     verbose_name="To Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="From Client")

    objects = BillQuerySet.as_manager()

    class Meta:
        ordering = ('-date_issued', 'id')


class BillLine(AbstractInvoiceLine):
    bill = models.ForeignKey('books.Bill',
                             related_name="lines")

    class Meta:
        pass
