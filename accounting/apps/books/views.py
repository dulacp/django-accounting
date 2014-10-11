from django.views import generic
from django.core.urlresolvers import reverse

from .models import User, Organization, Invoice


class DashboardView(generic.TemplateView):
    template_name = "books/dashboard.html"


class OrganizationListView(generic.ListView):
    template_name = "books/organization_list.html"
    model = Organization
    context_object_name = "organizations"


class OrganizationCreateView(generic.CreateView):
    template_name = "books/organization_create.html"
    model = Organization
    fields = (
        'display_name',
        'legal_name',
    )

    def get_success_url(self):
        return reverse("books:organization-list")


class OrganizationDetailView(generic.DetailView):
    template_name = "books/organization_detail.html"
    model = Organization
    context_object_name = "organization"


class InvoiceListView(generic.ListView):
    template_name = "books/invoice_list.html"
    model = Invoice
    context_object_name = "invoices"


class InvoiceCreateView(generic.CreateView):
    template_name = "books/invoice_create.html"
    model = Invoice
