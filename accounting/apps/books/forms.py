from django.forms import ModelForm, BaseInlineFormSet
from django.forms.models import inlineformset_factory

from .models import (
    Organization,
    TaxRate,
    TaxComponent,
    Invoice,
    InvoiceLine,
    Bill,
    BillLine,
    Payment)


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


class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = (
            "display_name",
            "legal_name",
        )


class TaxRateForm(ModelForm):
    class Meta:
        model = TaxRate
        fields = (
            "name",
            "organization",
        )


class TaxComponentForm(ModelForm):
    class Meta:
        model = TaxComponent
        fields = (
            "name",
            "percentage",
        )


TaxComponentFormSet = inlineformset_factory(TaxRate,
                                            TaxComponent,
                                            form=TaxComponentForm,
                                            formset=RequiredFirstInlineFormSet,
                                            min_num=1,
                                            extra=0)


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            "number",
            "organization",
            "client",

            "draft",
            "sent",
            "paid",
            "date_issued",
            "date_dued",
        )


class InvoiceLineForm(ModelForm):
    class Meta:
        model = InvoiceLine
        fields = (
            "label",
            "description",
            "unit_price_excl_tax",
            "quantity",
        )


InvoiceLineFormSet = inlineformset_factory(Invoice,
                                           InvoiceLine,
                                           form=InvoiceLineForm,
                                           formset=RequiredFirstInlineFormSet,
                                           extra=1)


class BillForm(ModelForm):
    class Meta:
        model = Bill
        fields = (
            "number",
            "client",
            "organization",

            "draft",
            "sent",
            "paid",
            "date_issued",
            "date_dued",
        )


class BillLineForm(ModelForm):
    class Meta:
        model = BillLine
        fields = (
            "label",
            "description",
            "unit_price_excl_tax",
            "quantity",
        )


BillLineFormSet = inlineformset_factory(Bill,
                                        BillLine,
                                        form=BillLineForm,
                                        formset=RequiredFirstInlineFormSet,
                                        extra=1)


class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = (
            "amount",
            "reference",
            "detail",
            "date_paid",
        )
