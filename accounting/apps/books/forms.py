from django.forms import ModelForm, BaseFormSet
from django.forms.models import inlineformset_factory

from .models import Invoice, InvoiceLine


class RequiredFormSet(BaseFormSet):
    """
    Used to make empty formset forms required
    See http://stackoverflow.com/questions/2406537/django-formsets-make-first-required/4951032#4951032
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False


class InvoiceForm(ModelForm):
    class Meta:
        model = Invoice
        fields = (
            # "number",
            "organization",
            "draft",
            "sent",
            "paid",
            "date_issued",
            "date_paid",
        )


class InvoiceLineForm(ModelForm):
    class Meta:
        model = InvoiceLine
        fields = (
            "label",
            "description",
            "unit_price",
            "quantity",
        )


InvoiceLineFormSet = inlineformset_factory(Invoice,
                                           InvoiceLine,
                                           form=InvoiceLineForm,
                                           formset=RequiredFormSet,
                                           extra=1)
