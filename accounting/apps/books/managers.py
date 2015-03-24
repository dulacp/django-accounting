from datetime import date

from django.db import models
from django.db.models import Sum


class TotalQuerySetMixin(object):

    def _get_total(self, prop):
        return self.aggregate(sum=Sum(prop))["sum"]

    def total_paid(self):
        return self._get_total('payments__amount')


class InvoiceQuerySetMixin(object):

    def dued(self):
        return self.filter(date_dued__lte=date.today())


class EstimateQuerySet(TotalQuerySetMixin, models.QuerySet):
    pass


class InvoiceQuerySet(TotalQuerySetMixin,
                      InvoiceQuerySetMixin,
                      models.QuerySet):

    def turnover_excl_tax(self):
        return self._get_total('total_excl_tax')

    def turnover_incl_tax(self):
        return self._get_total('total_incl_tax')


class BillQuerySet(TotalQuerySetMixin,
                   InvoiceQuerySetMixin,
                   models.QuerySet):

    def debts_excl_tax(self):
        return self._get_total('total_excl_tax')

    def debts_incl_tax(self):
        return self._get_total('total_incl_tax')


class ExpenseClaimQuerySet(TotalQuerySetMixin,
                           InvoiceQuerySetMixin,
                           models.QuerySet):

    def debts_excl_tax(self):
        return self._get_total('total_excl_tax')

    def debts_incl_tax(self):
        return self._get_total('total_incl_tax')
