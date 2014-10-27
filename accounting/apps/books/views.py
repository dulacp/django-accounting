import logging

from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .mixins import (
    SelectedOrganizationMixin,
    RestrictToSelectedOrganizationQuerySetMixin,
    AbstractSaleCreateUpdateMixin,
    AbstractSaleDetailMixin,
    TaxRateCreateUpdateMixin,
    PaymentFormMixin)
from .models import (
    Organization,
    TaxRate,
    TaxComponent,
    Estimate,
    Invoice,
    Bill,
    Payment)
from .forms import (
    OrganizationForm,
    TaxRateForm,
    TaxComponentFormSet,
    EstimateForm,
    EstimateLineFormSet,
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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        organization = self.get_object()
        ctx['invoices'] = (organization.invoices.all()
            .select_related(
                'client',
                'organization')
            .prefetch_related(
                'lines',
                'lines__tax_rate',
                'lines__tax_rate__components',
                'payments'))
        ctx['bills'] = (organization.bills.all()
            .select_related(
                'client',
                'organization')
            .prefetch_related(
                'lines',
                'lines__tax_rate',
                'lines__tax_rate__components',
                'payments'))
        return ctx

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

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        organization = self.get_object()
        ctx['invoices'] = (organization.invoices.all()
            .select_related('client', 'organization')
            .prefetch_related('lines'))
        ctx['bills'] = (organization.bills.all()
            .select_related('client', 'organization')
            .prefetch_related('lines'))
        return ctx


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


class TaxRateCreateView(TaxRateCreateUpdateMixin, generic.CreateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm
    formset_class = TaxComponentFormSet

    def get_success_url(self):
        return reverse("books:tax_rate-list")


class TaxRateUpdateView(TaxRateCreateUpdateMixin, generic.UpdateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm
    formset_class = TaxComponentFormSet

    def get_success_url(self):
        return reverse("books:tax_rate-list")


class TaxRateDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = TaxRate
    success_url = reverse_lazy('books:tax_rate-list')


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


class EstimateListView(SelectedOrganizationMixin,
                       RestrictToSelectedOrganizationQuerySetMixin,
                       generic.ListView):
    template_name = "books/estimate_list.html"
    model = Estimate
    context_object_name = "estimates"


class EstimateCreateView(AbstractSaleCreateUpdateMixin,
                         generic.CreateView):
    template_name = "books/bill_create_or_update.html"
    model = Estimate
    form_class = EstimateForm
    formset_class = EstimateLineFormSet

    def get_success_url(self):
        return reverse("books:estimate-list")


class EstimateUpdateView(AbstractSaleCreateUpdateMixin,
                         generic.UpdateView):
    template_name = "books/estimate_create_or_update.html"
    model = Estimate
    form_class = EstimateForm
    formset_class = EstimateLineFormSet

    def get_success_url(self):
        return reverse("books:estimate-list")


class EstimateDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Estimate
    success_url = reverse_lazy('books:estimate-list')


class EstimateDetailView(AbstractSaleDetailMixin,
                         generic.DetailView):
    template_name = "books/estimate_detail.html"
    model = Estimate
    context_object_name = "estimate"

    def get_success_url(self):
        return reverse('books:estimate-detail', args=[self.object.pk])


class InvoiceListView(SelectedOrganizationMixin,
                      RestrictToSelectedOrganizationQuerySetMixin,
                      generic.ListView):
    template_name = "books/invoice_list.html"
    model = Invoice
    context_object_name = "invoices"


class InvoiceCreateView(AbstractSaleCreateUpdateMixin,
                        generic.CreateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceLineFormSet

    def get_success_url(self):
        return reverse("books:invoice-list")


class InvoiceUpdateView(AbstractSaleCreateUpdateMixin,
                        generic.UpdateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceLineFormSet

    def get_success_url(self):
        return reverse("books:invoice-list")


class InvoiceDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Invoice
    success_url = reverse_lazy('books:invoice-list')


class InvoiceDetailView(PaymentFormMixin,
                        AbstractSaleDetailMixin,
                        generic.DetailView):
    template_name = "books/invoice_detail.html"
    model = Invoice
    context_object_name = "invoice"
    payment_form_class = PaymentForm

    def get_success_url(self):
        return reverse('books:invoice-detail', args=[self.object.pk])


class BillListView(SelectedOrganizationMixin,
                   RestrictToSelectedOrganizationQuerySetMixin,
                   generic.ListView):
    template_name = "books/bill_list.html"
    model = Bill
    context_object_name = "bills"


class BillCreateView(AbstractSaleCreateUpdateMixin,
                     generic.CreateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm
    formset_class = BillLineFormSet

    def get_success_url(self):
        return reverse("books:bill-list")


class BillUpdateView(AbstractSaleCreateUpdateMixin,
                     generic.UpdateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm
    formset_class = BillLineFormSet

    def get_success_url(self):
        return reverse("books:bill-list")


class BillDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = Bill
    success_url = reverse_lazy('books:bill-list')


class BillDetailView(PaymentFormMixin,
                     AbstractSaleDetailMixin,
                     generic.DetailView):
    template_name = "books/bill_detail.html"
    model = Bill
    context_object_name = "bill"
    payment_form_class = PaymentForm

    def get_success_url(self):
        return reverse('books:bill-detail', args=[self.object.pk])
