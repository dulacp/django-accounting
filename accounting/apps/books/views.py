from django.views import generic
from django.core.urlresolvers import reverse
from django.db.models import Count, Sum

from .models import User, Organization, Invoice, Bill
from .forms import (
    OrganizationForm,
    InvoiceForm,
    InvoiceLineFormSet,
    BillForm,
    BillLineFormSet)


class DashboardView(generic.TemplateView):
    template_name = "books/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orgas = Organization.objects.all()
        cumulated_turnovers = orgas.aggregate(sum=Sum('invoices__total_excl_tax'))["sum"]
        cumulated_debts = orgas.aggregate(sum=Sum('bills__total_excl_tax'))["sum"]
        cumulated_profits = cumulated_turnovers - cumulated_debts

        context["organizations_count"] = orgas.count()
        context["organizations_cumulated_turnovers"] = cumulated_turnovers
        context["organizations_cumulated_profits"] = cumulated_profits
        context["organizations_cumulated_active_days"] = 0

        context["last_invoices"] = Invoice.objects.all()[:10]

        return context


class OrganizationListView(generic.ListView):
    template_name = "books/organization_list.html"
    model = Organization
    context_object_name = "organizations"


class OrganizationCreateView(generic.CreateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse("books:organization-list")


class OrganizationUpdateView(generic.UpdateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm

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


class InvoiceCreateUpdateMixin(object):

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

        # update totals
        self.object.compute_totals()

        return super().form_valid(form)


class InvoiceCreateView(InvoiceCreateUpdateMixin, generic.CreateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse("books:invoice-list")


class InvoiceUpdateView(InvoiceCreateUpdateMixin, generic.UpdateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm

    def get_success_url(self):
        return reverse("books:invoice-list")


class BillListView(generic.ListView):
    template_name = "books/bill_list.html"
    model = Bill
    context_object_name = "bills"


class BillCreateUpdateMixin(object):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['billline_formset'] = BillLineFormSet(self.request.POST,
                                                             instance=self.object)
        else:
            context['billline_formset'] = BillLineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        billline_formset = context['billline_formset']
        if not billline_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        billline_formset.instance = self.object
        billline_formset.save()

        # update totals
        self.object.compute_totals()

        return super().form_valid(form)


class BillCreateView(BillCreateUpdateMixin, generic.CreateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm

    def get_success_url(self):
        return reverse("books:bill-list")


class BillUpdateView(BillCreateUpdateMixin, generic.UpdateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm

    def get_success_url(self):
        return reverse("books:bill-list")
