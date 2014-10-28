from datetime import date
from decimal import Decimal as D
from collections import defaultdict

from accounting.apps.books.models import Invoice, Bill
from accounting.libs import prices


class ReportPeriod(object):
    start = None
    end = None

    def __init__(self, start, end):
        assert isinstance(start, date), "start should be a date instance"
        assert isinstance(end, date), "end should be a date instance"
        self.start = start
        self.end = end


class BaseReport(object):
    title = None
    period = None

    def __init__(self, title, start, end):
        self.title = title
        self.period = ReportPeriod(start, end)

    def generate(self):
        raise NotImplementedError


class TaxRateSummary(object):
    tax_rate = None
    taxable_amount = D('0')
    expenses_amount = D('0')

    @property
    def collected_taxes(self):
        return self.tax_rate.rate * self.taxable_amount

    @property
    def deductible_taxes(self):
        return self.tax_rate.rate * self.expenses_amount

    @property
    def net_amount(self):
        return self.taxable_amount - self.expenses_amount

    @property
    def net_taxes(self):
        return self.tax_rate.rate * self.net_amount


class TaxReport(BaseReport):
    # TODO implement 'Billed (Accrual) / Collected (Cash based)'
    organization = None
    tax_summaries = None

    def __init__(self, organization, start, end):
        super().__init__("Tax Report", start, end)
        self.organization = organization
        self.tax_summaries = defaultdict(TaxRateSummary)

    def generate(self):
        invoice_queryset = Invoice.objects.all()
        bill_queryset = Bill.objects.all()
        self.generate_for_sales(invoice_queryset)
        self.generate_for_sales(bill_queryset)

    def generate_for_sales(self, sales_queryset):
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
                if pay.date_paid < self.period.start:
                    continue
                if pay.date_paid > self.period.end:
                    continue

                # compute the percentage of the amount paid
                # against each line amount
                for line in sale.lines.all():
                    tax_rate = line.tax_rate
                    line_factor = line.line_price_incl_tax / sale.total_incl_tax
                    portion_line_amount = pay.amount * line_factor
                    portion_taxable_amount = portion_line_amount / (D('1') + tax_rate.rate)

                    summary = self.tax_summaries[tax_rate.pk]
                    summary.tax_rate = tax_rate

                    if isinstance(sale, Invoice):
                        summary.taxable_amount += portion_taxable_amount
                    elif isinstance(sale, Bill):
                        summary.expenses_amount += portion_taxable_amount
                    else:
                        raise ValueError("Unsupported type of sale {}"
                            .format(sale.__class__))
