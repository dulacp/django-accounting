from datetime import date

from django.views import generic
from django.core.urlresolvers import reverse

from accounting.apps.books.utils import organization_manager
from .models import FinancialSettings
from .forms import FinancialSettingsForm
from .wrappers import TaxReport


class ReportListView(generic.TemplateView):
    template_name = "reports/report_list.html"


class SettingsListView(generic.TemplateView):
    template_name = "reports/settings_list.html"


class FinancialSettingsUpdateView(generic.UpdateView):
    template_name = "reports/financial_settings_update.html"
    model = FinancialSettings
    form_class = FinancialSettingsForm

    def get_object(self):
        orga = organization_manager.get_selected_organization(self.request)
        try:
            settings = orga.financial_settings
        except FinancialSettings.DoesNotExist:
            settings = FinancialSettings(organization=orga)
        return settings

    def get_success_url(self):
        return reverse("reports:settings-list")


class TaxReportView(generic.TemplateView):
    template_name = "reports/tax_report.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        orga = organization_manager.get_selected_organization(self.request)
        report = TaxReport(orga,
                           start=date(2014, 1, 1),
                           end=date(2014, 12, 1))
        report.generate()
        ctx['tax_summaries'] = report.tax_summaries.values()
        # ctx['report'] = TaxReport(start=None, end=None)
        return ctx
