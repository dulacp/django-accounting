from django.forms import ModelForm

from .models import FinancialSettings, PayRunSettings


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


class PayRunSettingsForm(ModelForm):
    class Meta:
        model = PayRunSettings
        fields = (
            "salaries_follow_profits",
            "payrun_period",
        )
