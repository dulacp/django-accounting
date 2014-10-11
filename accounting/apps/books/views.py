from django.views import generic
from django.core.urlresolvers import reverse

from .models import User, Organization


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
    context_object_name = "organization"

    def get_success_url(self):
        return reverse("books:organization-list")
