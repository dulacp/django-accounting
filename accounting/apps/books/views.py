from django.views import generic

from .models import User, Organization


class OrganizationListView(generic.ListView):
    template_name = "books/organization_list.html"
    model = Organization
