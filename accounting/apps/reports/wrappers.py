from decimal import Decimal as D
from collections import defaultdict, OrderedDict

from dateutil.relativedelta import relativedelta

from accounting.apps.books.models import Invoice, Bill
from accounting.apps.books.calculators import ProfitsLossCalculator
from accounting.libs import prices
from accounting.libs.intervals import TimeInterval


class BaseReport(object):
    title = None
    period = None

    def __init__(self, title, start, end):
        self.title = title
        self.period = TimeInterval(start, end)

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

                # NB: even with the queryset filters we can still get payments
                #     outside the period interval [start, end], because
                #     `self.payements.all()` is uncorrelated with the filters
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


class ProfitAndLossSummary(object):
    grouping_date = None
    sales_amount = D('0')
    expenses_amount = D('0')

    @property
    def net_profit(self):
        return self.sales_amount - self.expenses_amount


class ProfitAndLossReport(BaseReport):
    # TODO implement 'Billed (Accrual) / Collected (Cash based)'
    organization = None
    summaries = None
    total_summary = None

    RESOLUTION_MONTHLY = 'monthly'
    RESOLUTION_CHOICES = (
        RESOLUTION_MONTHLY,
    )
    group_by_resolution = RESOLUTION_MONTHLY

    def __init__(self, organization, start, end):
        super().__init__("Profit and Loss", start, end)
        self.organization = organization
        self.summaries = {}
        steps_interval = relativedelta(end, start)

        assert(self.group_by_resolution in self.RESOLUTION_CHOICES,
            "No a resolution choice")
        if self.group_by_resolution == self.RESOLUTION_MONTHLY:
            for step in range(0, steps_interval.months):
                key_date = start + relativedelta(months=step)
                self.summaries[key_date] = ProfitAndLossSummary()
        else:
            raise ValueError("Unsupported resolution {}"
                .format(self.group_by_resolution))

        self.total_summary = ProfitAndLossSummary()

    def group_by_date(self, date):
        if self.group_by_resolution == self.RESOLUTION_MONTHLY:
            grouping_date = date.replace(day=1)
        else:
            raise ValueError("Unsupported resolution {}"
                .format(self.group_by_resolution))
        return grouping_date

    def generate(self):
        invoice_queryset = Invoice.objects.all()
        bill_queryset = Bill.objects.all()
        self.generate_for_sales(invoice_queryset)
        self.generate_for_sales(bill_queryset)

        # order the results
        self.summaries = OrderedDict(sorted(self.summaries.items()))

        # compute totals
        for summary in self.summaries.values():
            self.total_summary.sales_amount += summary.sales_amount
            self.total_summary.expenses_amount += summary.expenses_amount

    def generate_for_sales(self, sales_queryset):
        calculator = ProfitsLossCalculator(self.organization,
                                           start=self.period.start,
                                           end=self.period.end)

        for sale, payment, amount_excl_tax in calculator.process_generator(sales_queryset):
            key_date = self.group_by_date(payment.date_paid)
            summary = self.summaries[key_date]

            if isinstance(sale, Invoice):
                summary.sales_amount += amount_excl_tax
            elif isinstance(sale, Bill):
                summary.expenses_amount += amount_excl_tax
            else:
                raise ValueError("Unsupported type of sale {}"
                    .format(sale.__class__))


class PayRunSummary(object):
    payroll_tax_rate = None
    total_excl_tax = D('0')

    @property
    def payroll_taxes(self):
        return self.payroll_tax_rate * self.total_excl_tax


class PayRunReport(BaseReport):
    organization = None
    summaries = None
    total_payroll_taxes = D('0')

    def __init__(self, organization, start, end):
        super().__init__("Pay Run Report", start, end)
        self.organization = organization
        self.summaries = defaultdict(PayRunSummary)

    def generate(self):
        employee_queryset = self.organization.employees.all()
        self.generate_for_employees(employee_queryset)

    def generate_for_employees(self, employee_queryset):
        total_payroll_taxes = D('0')
        calculator = ProfitsLossCalculator(self.organization,
                                           start=self.period.start,
                                           end=self.period.end)

        for emp in employee_queryset:
            summary = self.summaries[emp.composite_name]
            summary.employee = emp
            summary.payroll_tax_rate = emp.payroll_tax_rate
            if emp.salary_follows_profits:
                # TODO compute profits based on the period interval
                profits = calculator.profits()
                summary.total_excl_tax = profits * emp.shares_percentage
            else:
                raise ValueError("Salary not indexed on the profits "
                                 "are not supported yet")

            total_payroll_taxes += summary.payroll_taxes

        # Total payroll
        self.total_payroll_taxes = total_payroll_taxes
