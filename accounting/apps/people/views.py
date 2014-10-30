from django.views import generic
from django.core.urlresolvers import reverse

from accounting.apps.books.mixins import (
    RestrictToSelectedOrganizationQuerySetMixin,
    AutoSetSelectedOrganizationMixin)
from .models import Client, Employee
from .forms import ClientForm, EmployeeForm


class ClientListView(RestrictToSelectedOrganizationQuerySetMixin,
                     generic.ListView):
    template_name = "people/client_list.html"
    model = Client
    context_object_name = "clients"


class ClientCreateView(AutoSetSelectedOrganizationMixin,
                       generic.CreateView):
    template_name = "people/client_create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientUpdateView(RestrictToSelectedOrganizationQuerySetMixin,
                       AutoSetSelectedOrganizationMixin,
                       generic.UpdateView):
    template_name = "people/client_create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientDetailView(RestrictToSelectedOrganizationQuerySetMixin,
                       generic.DetailView):
    template_name = "people/client_detail.html"
    model = Client
    context_object_name = "client"


class EmployeeListView(RestrictToSelectedOrganizationQuerySetMixin,
                       generic.ListView):
    template_name = "people/employee_list.html"
    model = Employee
    context_object_name = "employees"


class EmployeeCreateView(AutoSetSelectedOrganizationMixin,
                         generic.CreateView):
    template_name = "people/employee_create_or_update.html"
    model = Employee
    form_class = EmployeeForm

    def get_success_url(self):
        return reverse("people:employee-list")


class EmployeeUpdateView(RestrictToSelectedOrganizationQuerySetMixin,
                         AutoSetSelectedOrganizationMixin,
                         generic.UpdateView):
    template_name = "people/employee_create_or_update.html"
    model = Employee
    form_class = EmployeeForm

    def get_success_url(self):
        return reverse("people:employee-list")


class EmployeeDetailView(RestrictToSelectedOrganizationQuerySetMixin,
                         generic.DetailView):
    template_name = "people/employee_detail.html"
    model = Employee
    context_object_name = "employee"
