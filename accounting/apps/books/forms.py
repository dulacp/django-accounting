from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import (
    Organization,
    TaxRate,
    Estimate,
    EstimateLine,
    Invoice,
    InvoiceLine,
    Bill,
    BillLine,
    Payment)
from .utils import organization_manager
from accounting.apps.people.models import Client
from accounting.apps.people.forms import UserMultipleChoices

from django_select2.fields import AutoModelSelect2Field
from datetimewidget.widgets import DateWidget


class RequiredFirstInlineFormSet(BaseInlineFormSet):
    """
    Used to make empty formset forms required
    See http://stackoverflow.com/questions/2406537/django-formsets-\
        make-first-required/4951032#4951032
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if len(self.forms) > 0:
            first_form = self.forms[0]
            first_form.empty_permitted = False


class SaleInlineLineFormSet(RequiredFirstInlineFormSet):

    def __init__(self, *args, **kwargs):
        orga = kwargs.pop('organization')
        super().__init__(*args, **kwargs)
        for f in self.forms:
            f.restrict_to_organization(orga)


class ClientForOrganizationChoices(AutoModelSelect2Field):
    queryset = Client.objects.all()
    search_fields = (
        'name__icontains',
    )

    def prepare_qs_params(self, request, search_term, search_fields):
        """restrict to the current selected organization"""
        params = super().prepare_qs_params(request, search_term, search_fields)
        orga = organization_manager.get_selected_organization(request)
        params['and']['organization'] = orga
        return params


class OrganizationForm(ModelForm):
    members = UserMultipleChoices(required=False)

    class Meta:
        model = Organization
        fields = (
            "display_name",
            "legal_name",
            "members",
        )


class TaxRateForm(ModelForm):
    class Meta:
        model = TaxRate
        fields = (
            "name",
            "rate",
        )


class RestrictLineFormToOrganizationMixin(object):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance:
            if isinstance(instance, InvoiceLine):
                organization = instance.invoice.organization
            elif isinstance(instance, BillLine):
                organization = instance.bill.organization
            else:
                raise NotImplementedError("The mixin has been applied to a "
                                          "form model that is not supported")
            self.restrict_to_organization(organization)

    def restrict_to_organization(self, organization):
        self.fields['tax_rate'].queryset = organization.tax_rates.all()


class EstimateForm(ModelForm):
    client = ClientForOrganizationChoices()

    class Meta:
        model = Estimate
        fields = (
            "number",
            "client",
            "date_issued",
            "date_dued",
        )
        widgets = {
            'date_issued': DateWidget(
                attrs={'id': "id_date_issued"},
                usel10n=True,
                bootstrap_version=3),
            'date_dued': DateWidget(
                attrs={'id': "id_date_dued"},
                usel10n=True,
                bootstrap_version=3),
        }


class EstimateLineForm(RestrictLineFormToOrganizationMixin,
                       ModelForm):
    class Meta:
        model = EstimateLine
        fields = (
            "label",
            "description",
            "unit_price_excl_tax",
            "quantity",
            "tax_rate",
        )


EstimateLineFormSet = inlineformset_factory(Estimate,
                                            EstimateLine,
                                            form=EstimateLineForm,
                                            formset=SaleInlineLineFormSet,
                                            min_num=1,
                                            extra=0)


class InvoiceForm(ModelForm):
    client = ClientForOrganizationChoices()

    class Meta:
        model = Invoice
        fields = (
            "number",
            "client",
            "date_issued",
            "date_dued",
        )
        widgets = {
            'date_issued': DateWidget(
                attrs={'id': "id_date_issued"},
                usel10n=True,
                bootstrap_version=3),
            'date_dued': DateWidget(
                attrs={'id': "id_date_dued"},
                usel10n=True,
                bootstrap_version=3),
        }


class InvoiceLineForm(RestrictLineFormToOrganizationMixin,
                      ModelForm):
    class Meta:
        model = InvoiceLine
        fields = (
            "label",
            "description",
            "unit_price_excl_tax",
            "quantity",
            "tax_rate",
        )


InvoiceLineFormSet = inlineformset_factory(Invoice,
                                           InvoiceLine,
                                           form=InvoiceLineForm,
                                           formset=SaleInlineLineFormSet,
                                           min_num=1,
                                           extra=0)


class BillForm(ModelForm):
    client = ClientForOrganizationChoices()

    class Meta:
        model = Bill
        fields = (
            "number",
            "client",
            "date_issued",
            "date_dued",
        )
        widgets = {
            'date_issued': DateWidget(
                attrs={'id': "id_date_issued"},
                usel10n=True,
                bootstrap_version=3),
            'date_dued': DateWidget(
                attrs={'id': "id_date_dued"},
                usel10n=True,
                bootstrap_version=3),
        }


class BillLineForm(RestrictLineFormToOrganizationMixin,
                   ModelForm):
    class Meta:
        model = BillLine
        fields = (
            "label",
            "description",
            "unit_price_excl_tax",
            "quantity",
            "tax_rate",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


BillLineFormSet = inlineformset_factory(Bill,
                                        BillLine,
                                        form=BillLineForm,
                                        formset=SaleInlineLineFormSet,
                                        min_num=1,
                                        extra=0)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = (
            "amount",
            "reference",
            "detail",
            "date_paid",
        )
        widgets = {
            'date_paid': DateWidget(
                attrs={'id': "id_date_paid"},
                usel10n=True,
                bootstrap_version=3),
        }
