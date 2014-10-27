from django.forms import ModelForm

from .models import FinancialSettings


class FinancialSettingsForm(ModelForm):
    class Meta:
        model = FinancialSettings
        fields = (
            "financial_year_end_day",
            "financial_year_end_month",

            "tax_id_number",
            "tax_id_display_name",
            "tax_period",
        )
