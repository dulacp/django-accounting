from django.forms import ModelForm

from .models import Client, Employee


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
            "organization",
        )


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee
        fields = (
            "first_name",
            "last_name",
            "email",

            "salary_follows_profits",
            "shares_percentage",

            "organization",
        )
