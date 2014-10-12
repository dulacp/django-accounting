from decimal import Decimal, ROUND_HALF_EVEN
from datetime import date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

from libs.utils import banker_round
from .managers import InvoiceQuerySet
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


class AbstractInvoice(models.Model):
    number = models.CharField(max_length=6,
                              unique=True,
                              default=next_invoice_number)

    # tracking
    draft = models.BooleanField(default=False)
    sent = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    date_issued = models.DateField(default=date.today)
    date_paid = models.DateField(blank=True, null=True)

    objects = InvoiceQuerySet.as_manager()

    class Meta:
        abstract = True

    def __str__(self):
        return "#{} ({})".format(self.number, self.total())

    def total(self):
        total = Decimal('0.00')
        for item in self.lines.all():
            total = total + item.total()
        return total


class AbstractInvoiceLine(models.Model):
    label = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=8,
                                     decimal_places=2)
    quantity = models.DecimalField(max_digits=8,
                                   decimal_places=2,
                                   default=1)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label

    def total(self):
        total = self.unit_price * self.quantity
        return banker_round(total)


class Invoice(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     verbose_name="From Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="To Client")

    class Meta:
        ordering = ('-date_issued', 'id')


class InvoiceLine(AbstractInvoiceLine):
    invoice = models.ForeignKey('books.Invoice',
                                related_name="lines")

    class Meta:
        pass


class Bill(AbstractInvoice):
    organization = models.ForeignKey('books.Organization',
                                     verbose_name="To Organization")
    client = models.ForeignKey('clients.Client',
                               verbose_name="From Client")

    class Meta:
        ordering = ('-date_issued', 'id')


class BillLine(AbstractInvoiceLine):
    bill = models.ForeignKey('books.Bill',
                             related_name="lines")

    class Meta:
        pass
