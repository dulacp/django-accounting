from decimal import Decimal as D
from collections import defaultdict, OrderedDict

from dateutil.relativedelta import relativedelta

from accounting.apps.books.models import Invoice, Bill
from accounting.apps.books.calculators import ProfitsLossCalculator
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
        calculator = ProfitsLossCalculator(self.organization,
                                           start=self.period.start,
                                           end=self.period.end)

        for output in calculator.process_generator(sales_queryset):
            summary = self.tax_summaries[output.tax_rate.pk]
            summary.tax_rate = output.tax_rate

            if isinstance(output.sale, Invoice):
                summary.taxable_amount += output.amount_excl_tax
            elif isinstance(output.sale, Bill):
                summary.expenses_amount += output.amount_excl_tax
            else:
                raise ValueError("Unsupported type of sale {}"
                    .format(output.sale.__class__))


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

        assert self.group_by_resolution in self.RESOLUTION_CHOICES, \
            "No a resolution choice"
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

        for output in calculator.process_generator(sales_queryset):
            key_date = self.group_by_date(output.payment.date_paid)
            summary = self.summaries[key_date]

            if isinstance(output.sale, Invoice):
                summary.sales_amount += output.amount_excl_tax
            elif isinstance(output.sale, Bill):
                summary.expenses_amount += output.amount_excl_tax
            else:
                raise ValueError("Unsupported type of sale {}"
                    .format(output.sale.__class__))


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


class InvoiceDetailsReport(BaseReport):
    organization = None
    invoices = None
    tax_rates = None

    def __init__(self, organization, start, end):
        super().__init__("Pay Run Report", start, end)
        self.organization = organization
        self.tax_rates = organization.tax_rates.all()

    def generate(self):
        invoice_queryset = self.organization.invoices.all()
        self.generate_for_invoices(invoice_queryset)

    def generate_for_invoices(self, invoice_queryset):
        invoice_queryset = (invoice_queryset
            .filter(payments__date_paid__range=[
                self.period.start,
                self.period.end
            ]))

        # optimize the query
        invoice_queryset = (invoice_queryset
            .select_related(
                'organization')
            .prefetch_related(
                'lines',
                'lines__tax_rate',
                'payments',
                'organization__employees',)
            .distinct())

        self.invoices = invoice_queryset
