from decimal import Decimal as D

from accounting.libs.intervals import TimeInterval


class SalePaymentLineProcessed(object):
    sale = None
    payment = None
    amount_excl_tax = None
    tax_rate = None

    def __init__(self, sale, payment):
        self.sale = sale
        self.payment = payment
        self.amount_excl_tax = D('0')

    def process(self):
        for line in self.sale.lines.all():
            tax_rate = line.tax_rate
            line_factor = line.line_price_incl_tax / self.sale.total_incl_tax
            portion_amount = self.payment.amount * line_factor
            portion_amount_excl_tax = portion_amount / (D('1') + tax_rate.rate)

            if self.tax_rate is None:
                self.tax_rate = tax_rate
            elif self.tax_rate.pk != tax_rate.pk:
                raise NotImplementedError("the system doesn't support "
                                          "yet multiple tax rates "
                                          "into a same invoice")

            self.amount_excl_tax += portion_amount_excl_tax


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

    def __init__(self, organization, sum_type=SUM_TYPE_COLLECTED,
                 start=None, end=None):
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
        sales_queryset = sales_queryset.filter(organization=self.organization)

        if self.period.start:
            sales_queryset = (sales_queryset
                .filter(payments__date_paid__gte=self.period.start))

        if self.period.end:
            sales_queryset = (sales_queryset
                .filter(payments__date_paid__lte=self.period.end))

        # optimize the queryset
        sales_queryset = (sales_queryset
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
                if self.period.start and pay.date_paid < self.period.start:
                    continue
                if self.period.end and pay.date_paid > self.period.end:
                    continue

                output = SalePaymentLineProcessed(sale, pay)
                output.process()

                yield output

    def total_collected(self):
        collected = D('0')
        invoices_queryset = self.organization.invoices.all()
        for output in self.process_generator(invoices_queryset):
            collected += output.amount_excl_tax
        return collected

    def total_expenses(self):
        expenses = D('0')
        bills_queryset = self.organization.bills.all()
        for output in self.process_generator(bills_queryset):
            expenses += output.amount_excl_tax
        return expenses

    def profits(self):
        return self.total_collected() - self.total_expenses()
