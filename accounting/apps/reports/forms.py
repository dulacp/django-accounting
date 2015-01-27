from datetime import timedelta

from django import forms

from .models import (
    BusinessSettings,
    FinancialSettings,
    PayRunSettings)


class BusinessSettingsForm(forms.ModelForm):
    class Meta:
        model = BusinessSettings
        fields = (
            "business_type",
        )


class FinancialSettingsForm(forms.ModelForm):
    class Meta:
        model = FinancialSettings
        fields = (
            "financial_year_end_day",
            "financial_year_end_month",

            "tax_id_number",
            "tax_id_display_name",
            "tax_period",
        )


class PayRunSettingsForm(forms.ModelForm):
    class Meta:
        model = PayRunSettings
        fields = (
            "salaries_follow_profits",
            "payrun_period",
        )


class TimePeriodForm(forms.Form):
    date_from = forms.DateField(required=False,
                                label="From")
    date_to = forms.DateField(required=False,
                              label="To")

    _filters = None
    _description = None

    def _determine_filter_metadata(self):
        self._filters = {}
        self._description = "All orders"
        if self.errors:
            return

        date_from = self.cleaned_data['date_from']
        date_to = self.cleaned_data['date_to']
        if date_from and date_to:
            # We want to include end date so we adjust the date we
            # use with the 'range' function.
            self._filters = {
                'date_placed__range': [
                    date_from,
                    date_to + timedelta(days=1)
                ]
            }
            self._description = ("Between {} and {}"
                .format(date_from, date_to))
        elif date_from and not date_to:
            self._filters = {'date_placed__gte': date_from}
            self._description = "Since {}".format(date_from)
        elif not date_from and date_to:
            self._filters = {'date_placed__lte': date_to}
            self._description = "Until {}".format(date_to)
        else:
            self._filters = {}
            self._description = "From the begining to now"

    def get_filters(self):
        if self._filters is None:
            self._determine_filter_metadata()
        return self._filters

    def get_filter_description(self):
        if self._description is None:
            self._determine_filter_metadata()
        return self._description
