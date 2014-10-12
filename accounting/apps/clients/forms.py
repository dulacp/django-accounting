from django.forms import ModelForm

from .models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = (
            "name",
            "address_line_1",
            "address_line_2",
            "city",
            "postal_code",
            "country",
        )
