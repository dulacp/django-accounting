from django.views import generic
from django.core.urlresolvers import reverse

from accounting.apps.books.utils import organization_manager
from .models import FinancialSettings
from .forms import FinancialSettingsForm


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
