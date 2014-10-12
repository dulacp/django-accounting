from datetime import date

from django.db import models
from django.db.models import Sum


class InvoiceQuerySetMixin(object):
    def draft(self):
        return self.filter(draft=True)

    def dued(self):
        return self.filter(date_issued__lte=date.today(),
                           draft=False,
                           paid=False)


class InvoiceQuerySet(InvoiceQuerySetMixin, models.QuerySet):

    @property
    def turnover(self):
        return self.aggregate(sum=Sum('total_excl_tax'))["sum"]


class BillQuerySet(InvoiceQuerySetMixin, models.QuerySet):

    @property
    def debts(self):
        return self.aggregate(sum=Sum('total_excl_tax'))["sum"]
