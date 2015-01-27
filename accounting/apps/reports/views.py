from datetime import date

from django.views import generic
from django.core.urlresolvers import reverse
from django.utils import timezone

from dateutil.relativedelta import relativedelta

from accounting.apps.books.utils import organization_manager
from accounting.libs.intervals import TimeInterval
from .models import (
    BusinessSettings,
    FinancialSettings,
    PayRunSettings)
from .forms import (
    BusinessSettingsForm,
    FinancialSettingsForm,
    PayRunSettingsForm,
    TimePeriodForm)
from .wrappers import (
    TaxReport,
    ProfitAndLossReport,
    PayRunReport,
    InvoiceDetailsReport)


class TimePeriodFormMixin(object):

    period = None

    def get_initial(self):
        initial = super().get_initial()

        # currrent quarter
        now = timezone.now()
        start = date(
            year=now.year,
            month=(now.month - ((now.month - 1) % 3)),
            day=1
        )
        end = start + relativedelta(months=3)

        initial['date_from'] = start
        initial['date_to'] = end

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.GET:
            kwargs.update({
                'data': self.request.GET,
            })
        return kwargs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        form = ctx['form']
        if form.is_valid():
            start = form.cleaned_data['date_from']
            end = form.cleaned_data['date_to']
            ctx['form_title'] = form.get_filter_description()
        else:
            start = end = None
            ctx['form_title'] = "Time Interval"

        if self.period is None:
            self.period = TimeInterval(start=start, end=end)

        return ctx


class ReportListView(generic.TemplateView):
    template_name = "reports/report_list.html"


class SettingsListView(generic.TemplateView):
    template_name = "reports/settings_list.html"


class GenericSettingsMixin(object):

    def get_object(self):
        orga = organization_manager.get_selected_organization(self.request)
        try:
            settings = self.model.objects.get(organization=orga)
        except self.model.DoesNotExist:
            settings = self.model.objects.create(organization=orga)
        return settings

    def get_success_url(self):
        return reverse("reports:settings-list")


class BusinessSettingsUpdateView(GenericSettingsMixin,
                                 generic.UpdateView):
    template_name = "reports/financial_settings_update.html"
    model = BusinessSettings
    form_class = BusinessSettingsForm


class FinancialSettingsUpdateView(GenericSettingsMixin,
                                  generic.UpdateView):
    template_name = "reports/financial_settings_update.html"
    model = FinancialSettings
    form_class = FinancialSettingsForm


class PayRunSettingsUpdateView(GenericSettingsMixin,
                               generic.UpdateView):
    template_name = "reports/payrun_settings_update.html"
    model = PayRunSettings
    form_class = PayRunSettingsForm


class TaxReportView(TimePeriodFormMixin,
                    generic.FormView):
    template_name = "reports/tax_report.html"
    form_class = TimePeriodForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orga = organization_manager.get_selected_organization(self.request)
        report = TaxReport(orga,
                           start=self.period.start,
                           end=self.period.end)
        report.generate()
        ctx['tax_summaries'] = report.tax_summaries.values()
        return ctx


class ProfitAndLossReportView(generic.TemplateView):
    template_name = "reports/profit_and_loss_report.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orga = organization_manager.get_selected_organization(self.request)

        # currrent quarter
        now = timezone.now()
        start = date(
            year=now.year,
            month=(now.month - ((now.month - 1) % 3)),
            day=1
        )
        end = start + relativedelta(months=3)

        report = ProfitAndLossReport(orga, start=start, end=end)
        report.generate()
        ctx['summaries'] = report.summaries
        ctx['total_summary'] = report.total_summary
        return ctx


class PayRunReportView(TimePeriodFormMixin,
                       generic.FormView):
    template_name = "reports/pay_run_report.html"
    form_class = TimePeriodForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orga = organization_manager.get_selected_organization(self.request)

        report = PayRunReport(orga,
                              start=self.period.start,
                              end=self.period.end)
        report.generate()
        ctx['summaries'] = report.summaries.values()
        ctx['total_payroll_taxes'] = report.total_payroll_taxes

        return ctx


class InvoiceDetailsView(TimePeriodFormMixin,
                         generic.FormView):
    template_name = "reports/invoice_details_report.html"
    form_class = TimePeriodForm

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orga = organization_manager.get_selected_organization(self.request)
        report = InvoiceDetailsReport(orga,
                                      start=self.period.start,
                                      end=self.period.end)
        report.generate()
        ctx['invoices'] = report.invoices
        ctx['tax_rates'] = report.tax_rates
        ctx['payrun_settings'] = orga.payrun_settings
        return ctx
