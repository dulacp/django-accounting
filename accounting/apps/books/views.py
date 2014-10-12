from django.views import generic
from django.core.urlresolvers import reverse

from .models import User, Organization, Invoice
from .forms import InvoiceForm, InvoiceLineFormSet


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
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse("books:invoice-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoiceline_formset'] = InvoiceLineFormSet(self.request.POST)
        else:
            context['invoiceline_formset'] = InvoiceLineFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        invoiceline_formset = context['invoiceline_formset']
        if not invoiceline_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        invoiceline_formset.instance = self.object
        invoiceline_formset.save()
        return super().form_valid(form)


class InvoiceUpdateView(generic.UpdateView):
    template_name = "books/invoice_create.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse("books:invoice-list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoiceline_formset'] = InvoiceLineFormSet(self.request.POST,
                                                                instance=self.object)
        else:
            context['invoiceline_formset'] = InvoiceLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        invoiceline_formset = context['invoiceline_formset']
        if not invoiceline_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        invoiceline_formset.instance = self.object
        invoiceline_formset.save()
        return super().form_valid(form)
