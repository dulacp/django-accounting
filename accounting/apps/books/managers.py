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

    def _get_total(self, prop):
        return self.aggregate(sum=Sum(prop))["sum"]

    def total_paid(self):
        return self._get_total('payments__amount')


class InvoiceQuerySet(InvoiceQuerySetMixin, models.QuerySet):

    def turnover_excl_tax(self):
        return self._get_total('total_excl_tax')

    def turnover_incl_tax(self):
        return self._get_total('total_incl_tax')


class BillQuerySet(InvoiceQuerySetMixin, models.QuerySet):

    def debts_excl_tax(self):
        return self._get_total('total_excl_tax')

    def debts_incl_tax(self):
        return self._get_total('total_incl_tax')
