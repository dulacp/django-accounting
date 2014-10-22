import logging

from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .mixins import (
    SelectedOrganizationMixin,
    RestrictToSelectedOrganizationQuerySetMixin)
from .models import (
    Organization,
    TaxRate,
    TaxComponent,
    Invoice,
    Bill,
    Payment)
from .forms import (
    OrganizationForm,
    TaxRateForm,
    TaxComponentFormSet,
    InvoiceForm,
    InvoiceLineFormSet,
    BillForm,
    BillLineFormSet,
    PaymentForm)

logger = logging.getLogger(__name__)


class OrganizationSelectorView(generic.TemplateView):
    template_name = "books/organization_selector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orgas = Organization.objects.all()
        cumulated_turnovers = (orgas
            .aggregate(sum=Sum('invoices__total_excl_tax'))["sum"])
        cumulated_debts = (orgas
            .aggregate(sum=Sum('bills__total_excl_tax'))["sum"])
        cumulated_profits = cumulated_turnovers - cumulated_debts

        context["organizations_count"] = orgas.count()
        context["organizations_cumulated_turnovers"] = cumulated_turnovers
        context["organizations_cumulated_profits"] = cumulated_profits
        context["organizations_cumulated_active_days"] = 0

        context["organizations"] = orgas
        context["last_invoices"] = Invoice.objects.all()[:10]

        return context


class DashboardView(SelectedOrganizationMixin,
                    generic.DetailView):
    template_name = "books/dashboard.html"
    model = Organization
    context_object_name = "organization"

    def get_object(self):
        return self.get_selected_organization()

    def get(self, request, *args, **kwargs):
        if self.get_selected_organization() is None:
            return HttpResponseRedirect(reverse('books:organization-selector'))
        return super().get(request, *args, **kwargs)


class OrganizationListView(generic.ListView):
    template_name = "books/organization_list.html"
    model = Organization
    context_object_name = "organizations"


class OrganizationCreateView(generic.CreateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("books:organization-list")


class OrganizationUpdateView(generic.UpdateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm

    def get_success_url(self):
        return reverse("books:organization-list")


class OrganizationDetailView(SelectedOrganizationMixin,
                             generic.DetailView):
    template_name = "books/organization_detail.html"
    model = Organization
    context_object_name = "organization"


class OrganizationSelectionView(SelectedOrganizationMixin,
                                generic.DetailView):
    model = Organization

    def post(self, request, *args, **kwargs):
        orga = self.get_object()
        self.set_selected_organization(orga)
        return HttpResponseRedirect(reverse('books:dashboard'))


class TaxRateListView(SelectedOrganizationMixin,
                      RestrictToSelectedOrganizationQuerySetMixin,
                      generic.ListView):
    template_name = "books/tax_rate_list.html"
    model = TaxRate
    context_object_name = "tax_rates"


class TaxRateCreateUpdateMixin(object):
    formset_class = TaxComponentFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['tax_component_formset'] = (
                self.formset_class(self.request.POST, instance=self.object))
        else:
            context['tax_component_formset'] = (
                self.formset_class(instance=self.object))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        tax_component_formset = context['tax_component_formset']
        if not tax_component_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        tax_component_formset.instance = self.object
        tax_component_formset.save()

        return super().form_valid(form)


class TaxRateCreateView(TaxRateCreateUpdateMixin, generic.CreateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm

    def get_success_url(self):
        return reverse("books:tax_rate-list")


class TaxRateUpdateView(TaxRateCreateUpdateMixin, generic.UpdateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm

    def get_success_url(self):
        return reverse("books:tax_rate-list")


class TaxRateDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = TaxRate
    success_url = reverse_lazy('books:tax_rate-list')


class PaymentFormMixin(generic.edit.FormMixin):
    form_class = PaymentForm

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context['form'] = form
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = self.get_object()

        # save payment
        payment = form.save(commit=False)
        payment.content_object = self.object
        payment.save()
        return super().form_valid(form)


class PaymentUpdateView(generic.UpdateView):
    template_name = "books/payment_create_or_update.html"
    model = Payment
    form_class = PaymentForm

    def get_success_url(self):
        related_obj = self.object.content_object
        if isinstance(related_obj, Invoice):
            return reverse("books:invoice-detail", args=[related_obj.pk])
        elif isinstance(related_obj, Bill):
            return reverse("books:bill-detail", args=[related_obj.pk])

        logger.warning("Unsupported related object '{}' for "
                       "payment '{}'".format(self.object, related_obj))
        return reverse("books:dashboard")


class PaymentDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Payment
    success_url = reverse_lazy('books:invoice-list')


class InvoiceListView(SelectedOrganizationMixin,
                      RestrictToSelectedOrganizationQuerySetMixin,
                      generic.ListView):
    template_name = "books/invoice_list.html"
    model = Invoice
    context_object_name = "invoices"


class InvoiceCreateUpdateMixin(object):
    formset_class = InvoiceLineFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['invoiceline_formset'] = (
                self.formset_class(self.request.POST, instance=self.object))
        else:
            context['invoiceline_formset'] = (
                self.formset_class(instance=self.object))
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


class InvoiceDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Invoice
    success_url = reverse_lazy('books:invoice-list')


class InvoiceDetailView(PaymentFormMixin,
                        generic.DetailView):
    template_name = "books/invoice_detail.html"
    model = Invoice
    context_object_name = "invoice"

    def get_success_url(self):
        return reverse('books:invoice-detail', args=[self.object.pk])


class BillListView(SelectedOrganizationMixin,
                   RestrictToSelectedOrganizationQuerySetMixin,
                   generic.ListView):
    template_name = "books/bill_list.html"
    model = Bill
    context_object_name = "bills"


class BillCreateUpdateMixin(object):
    formset_class = BillLineFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['billline_formset'] = (
                self.formset_class(self.request.POST, instance=self.object))
        else:
            context['billline_formset'] = (
                self.formset_class(instance=self.object))
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


class BillDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Bill
    success_url = reverse_lazy('books:bill-list')


class BillDetailView(PaymentFormMixin,
                     generic.DetailView):
    template_name = "books/bill_detail.html"
    model = Bill
    context_object_name = "bill"

    def get_success_url(self):
        return reverse('books:bill-detail', args=[self.object.pk])
