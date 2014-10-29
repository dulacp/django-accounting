from django.views import generic
from django.core.urlresolvers import reverse

from .models import Client
from .forms import ClientForm


class ClientListView(generic.ListView):
    template_name = "people/client_list.html"
    model = Client
    context_object_name = "clients"


class ClientCreateView(generic.CreateView):
    template_name = "people/client_create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientUpdateView(generic.UpdateView):
    template_name = "people/client_create_or_update.html"
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse("people:client-list")


class ClientDetailView(generic.DetailView):
    template_name = "people/client_detail.html"
    model = Client
    context_object_name = "client"
