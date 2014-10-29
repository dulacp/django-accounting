from decimal import Decimal as D

from django.db.models import Sum

from accounting.libs.intervals import TimeInterval


class ProfitsLossCalculator(object):
    """
    Compute the profits value in the most effective way
    considering the sum type (collected / accurial)
    and the given period of time.
    """

    # TODO support Accurial sum
    # SUM_TYPE_ACCURIAL = 'accurial'
    SUM_TYPE_COLLECTED = 'collected'
    SUM_TYPE_CHOICES = (
        # SUM_TYPE_ACCURIAL,
        SUM_TYPE_COLLECTED,
    )

    organization = None

    def __init__(self, organization, sum_type=SUM_TYPE_COLLECTED, start=None, end=None):
        assert sum_type in self.SUM_TYPE_CHOICES, "Not a supported sum type"
        self.organization = organization
        self.period = TimeInterval(start=start, end=end)

    def process_generator(self, sales_queryset):
        """
        Generator that computes the profits/loss for each sale payment objects

        It's a complex machine because of the partial payments that need
        to be taken into account with the sum type Collected.

        So it yield a tuple similar to

            (sale, payment, amount)

        """
        # optimize the queryset
        sales_queryset = (sales_queryset.filter(organization=self.organization)
            .filter(payments__date_paid__gte=self.period.start)
            .filter(payments__date_paid__lte=self.period.end)
            .prefetch_related(
                'lines',
                'lines__tax_rate',
                'payments')
            .distinct())

        for sale in sales_queryset:
            for pay in sale.payments.all():

                # NB: even with the queryset filters we can still get payments
                #     outside the period interval [start, end], because
                #     `self.payements.all()` is uncorrelated with the filters
                if pay.date_paid < self.period.start:
                    continue
                if pay.date_paid > self.period.end:
                    continue

                amount_excl_tax = D('0')
                for line in sale.lines.all():
                    tax_rate = line.tax_rate
                    line_factor = line.line_price_incl_tax / sale.total_incl_tax
                    portion_line_amount = pay.amount * line_factor
                    portion_amount_excl_tax = portion_line_amount / (D('1') + tax_rate.rate)

                    amount_excl_tax += portion_amount_excl_tax

                yield sale, pay, amount_excl_tax

    def total_collected(self):
        collected = D('0')
        invoices_queryset = self.organization.invoices.all()
        for inv, payment, amount_excl_tax in self.process_generator(invoices_queryset):
            collected += amount_excl_tax
        return collected

    def total_expenses(self):
        expenses = D('0')
        bills_queryset = self.organization.bills.all()
        for bill, payment, amount_excl_tax in self.process_generator(bills_queryset):
            expenses += amount_excl_tax
        return expenses

    def profits(self):
        return self.total_collected() - self.total_expenses()
