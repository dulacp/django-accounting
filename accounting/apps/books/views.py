import logging
from decimal import Decimal as D

from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.db.models import Sum
from django.http import HttpResponseRedirect

from .mixins import (
    RestrictToSelectedOrganizationQuerySetMixin,
    SaleListQuerySetMixin,
    AutoSetSelectedOrganizationMixin,
    AbstractSaleCreateUpdateMixin,
    AbstractSaleDetailMixin,
    PaymentFormMixin)
from .models import (
    Organization,
    TaxRate,
    Estimate,
    Invoice,
    Bill,
    ExpenseClaim,
    Payment)
from .forms import (
    OrganizationForm,
    TaxRateForm,
    EstimateForm,
    EstimateLineFormSet,
    InvoiceForm,
    InvoiceLineFormSet,
    BillForm,
    BillLineFormSet,
    ExpenseClaimForm,
    ExpenseClaimLineFormSet,
    PaymentForm)
from .utils import (
    organization_manager,
    EstimateNumberGenerator,
    InvoiceNumberGenerator,
    BillNumberGenerator,
    ExpenseClaimNumberGenerator)

logger = logging.getLogger(__name__)


class OrganizationSelectorView(generic.TemplateView):
    template_name = "books/organization_selector.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        orgas = organization_manager.get_user_organizations(user)
        cumulated_turnovers = (orgas
            .aggregate(sum=Sum('invoices__total_excl_tax'))["sum"]) or D('0')
        cumulated_debts = (orgas
            .aggregate(sum=Sum('bills__total_excl_tax'))["sum"]) or D('0')
        cumulated_profits = cumulated_turnovers - cumulated_debts

        context["organizations_count"] = orgas.count()
        context["organizations_cumulated_turnovers"] = cumulated_turnovers
        context["organizations_cumulated_profits"] = cumulated_profits
        context["organizations_cumulated_active_days"] = 0

        context["organizations"] = orgas
        context["last_invoices"] = Invoice.objects.all()[:10]

        return context


class DashboardView(generic.DetailView):
    template_name = "books/dashboard.html"
    model = Organization
    context_object_name = "organization"

    def get_object(self):
        return organization_manager.get_selected_organization(self.request)

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
                'payments')
            .distinct())
        ctx['bills'] = (organization.bills.all()
            .select_related(
                'client',
                'organization')
            .prefetch_related(
                'lines',
                'lines__tax_rate',
                'payments')
            .distinct())
        return ctx

    def get(self, request, *args, **kwargs):
        orga = organization_manager.get_selected_organization(self.request)
        if orga is None:
            return HttpResponseRedirect(reverse('books:organization-selector'))
        return super().get(request, *args, **kwargs)


class OrganizationListView(generic.ListView):
    template_name = "books/organization_list.html"
    model = Organization
    context_object_name = "organizations"

    def get_queryset(self):
        # only current authenticated user organizations
        return organization_manager.get_user_organizations(self.request.user)


class OrganizationCreateView(generic.CreateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy("books:organization-list")

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super().form_valid(form)


class OrganizationUpdateView(generic.UpdateView):
    template_name = "books/organization_create_or_update.html"
    model = Organization
    form_class = OrganizationForm
    success_url = reverse_lazy("books:organization-list")

    def get_queryset(self):
        # only current authenticated user organizations
        return organization_manager.get_user_organizations(self.request.user)


class OrganizationDetailView(generic.DetailView):
    template_name = "books/organization_detail.html"
    model = Organization
    context_object_name = "organization"

    def get_queryset(self):
        # only current authenticated user organizations
        return organization_manager.get_user_organizations(self.request.user)

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


class OrganizationSelectionView(generic.DetailView):
    model = Organization

    def get_queryset(self):
        # only current authenticated user organizations
        return organization_manager.get_user_organizations(self.request.user)

    def post(self, request, *args, **kwargs):
        orga = self.get_object()
        organization_manager.set_selected_organization(self.request, orga)
        return HttpResponseRedirect(reverse('books:dashboard'))


class TaxRateListView(RestrictToSelectedOrganizationQuerySetMixin,
                      generic.ListView):
    template_name = "books/tax_rate_list.html"
    model = TaxRate
    context_object_name = "tax_rates"


class TaxRateCreateView(AutoSetSelectedOrganizationMixin,
                        generic.CreateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm
    success_url = reverse_lazy("books:tax_rate-list")


class TaxRateUpdateView(AutoSetSelectedOrganizationMixin,
                        generic.UpdateView):
    template_name = "books/tax_rate_create_or_update.html"
    model = TaxRate
    form_class = TaxRateForm
    success_url = reverse_lazy("books:tax_rate-list")


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


class EstimateListView(RestrictToSelectedOrganizationQuerySetMixin,
                       SaleListQuerySetMixin,
                       generic.ListView):
    template_name = "books/estimate_list.html"
    model = Estimate
    context_object_name = "estimates"


class EstimateCreateView(AutoSetSelectedOrganizationMixin,
                         AbstractSaleCreateUpdateMixin,
                         generic.CreateView):
    template_name = "books/bill_create_or_update.html"
    model = Estimate
    form_class = EstimateForm
    formset_class = EstimateLineFormSet
    success_url = reverse_lazy("books:estimate-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        orga = organization_manager.get_selected_organization(self.request)
        self.restrict_fields_choices_to_organization(form, orga)
        return form

    def get_initial(self):
        initial = super().get_initial()

        orga = organization_manager.get_selected_organization(self.request)
        initial['number'] = EstimateNumberGenerator().next_number(orga)

        return initial


class EstimateUpdateView(AutoSetSelectedOrganizationMixin,
                         AbstractSaleCreateUpdateMixin,
                         generic.UpdateView):
    template_name = "books/estimate_create_or_update.html"
    model = Estimate
    form_class = EstimateForm
    formset_class = EstimateLineFormSet
    success_url = reverse_lazy("books:estimate-list")


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


class InvoiceListView(RestrictToSelectedOrganizationQuerySetMixin,
                      SaleListQuerySetMixin,
                      generic.ListView):
    template_name = "books/invoice_list.html"
    model = Invoice
    context_object_name = "invoices"


class InvoiceCreateView(AutoSetSelectedOrganizationMixin,
                        AbstractSaleCreateUpdateMixin,
                        generic.CreateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceLineFormSet
    success_url = reverse_lazy("books:invoice-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        orga = organization_manager.get_selected_organization(self.request)
        self.restrict_fields_choices_to_organization(form, orga)
        return form

    def get_initial(self):
        initial = super().get_initial()

        orga = organization_manager.get_selected_organization(self.request)
        initial['number'] = InvoiceNumberGenerator().next_number(orga)

        return initial


class InvoiceUpdateView(AutoSetSelectedOrganizationMixin,
                        AbstractSaleCreateUpdateMixin,
                        generic.UpdateView):
    template_name = "books/invoice_create_or_update.html"
    model = Invoice
    form_class = InvoiceForm
    formset_class = InvoiceLineFormSet
    success_url = reverse_lazy("books:invoice-list")


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


class BillListView(RestrictToSelectedOrganizationQuerySetMixin,
                   SaleListQuerySetMixin,
                   generic.ListView):
    template_name = "books/bill_list.html"
    model = Bill
    context_object_name = "bills"


class BillCreateView(AutoSetSelectedOrganizationMixin,
                     AbstractSaleCreateUpdateMixin,
                     generic.CreateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm
    formset_class = BillLineFormSet
    success_url = reverse_lazy("books:bill-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        orga = organization_manager.get_selected_organization(self.request)
        self.restrict_fields_choices_to_organization(form, orga)
        return form

    def get_initial(self):
        initial = super().get_initial()

        orga = organization_manager.get_selected_organization(self.request)
        initial['number'] = BillNumberGenerator().next_number(orga)

        return initial


class BillUpdateView(AutoSetSelectedOrganizationMixin,
                     AbstractSaleCreateUpdateMixin,
                     generic.UpdateView):
    template_name = "books/bill_create_or_update.html"
    model = Bill
    form_class = BillForm
    formset_class = BillLineFormSet
    success_url = reverse_lazy("books:bill-list")


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


class ExpenseClaimListView(RestrictToSelectedOrganizationQuerySetMixin,
                           SaleListQuerySetMixin,
                           generic.ListView):
    template_name = "books/expense_claim_list.html"
    model = ExpenseClaim
    context_object_name = "expense_claims"


class ExpenseClaimCreateView(AutoSetSelectedOrganizationMixin,
                             AbstractSaleCreateUpdateMixin,
                             generic.CreateView):
    template_name = "books/expense_claim_create_or_update.html"
    model = ExpenseClaim
    form_class = ExpenseClaimForm
    formset_class = ExpenseClaimLineFormSet
    success_url = reverse_lazy("books:expense_claim-list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        orga = organization_manager.get_selected_organization(self.request)
        self.restrict_fields_choices_to_organization(form, orga)
        return form

    def get_initial(self):
        initial = super().get_initial()

        orga = organization_manager.get_selected_organization(self.request)
        initial['number'] = ExpenseClaimNumberGenerator().next_number(orga)

        return initial


class ExpenseClaimUpdateView(AutoSetSelectedOrganizationMixin,
                             AbstractSaleCreateUpdateMixin,
                             generic.UpdateView):
    template_name = "books/expense_claim_create_or_update.html"
    model = ExpenseClaim
    form_class = ExpenseClaimForm
    formset_class = ExpenseClaimLineFormSet
    success_url = reverse_lazy("books:expense_claim-list")


class ExpenseClaimDeleteView(generic.DeleteView):
    template_name = "_generics/delete_entity.html"
    model = ExpenseClaim
    success_url = reverse_lazy('books:expense_claim-list')


class ExpenseClaimDetailView(PaymentFormMixin,
                             AbstractSaleDetailMixin,
                             generic.DetailView):
    template_name = "books/expense_claim_detail.html"
    model = ExpenseClaim
    context_object_name = "expense_claim"
    payment_form_class = PaymentForm

    def get_success_url(self):
        return reverse('books:expense_claim-detail', args=[self.object.pk])
