from django.db.models.fields import FieldDoesNotExist
from django.views import generic

from .models import Organization
from .utils import organization_manager


class RestrictToSelectedOrganizationQuerySetMixin(object):
    """
    To restrict objects to the current selected organization
    """

    def get_restriction_filters(self):
        # check for the field
        meta = self.model._meta
        field, model, direct, m2m = meta.get_field_by_name('organization')

        # build the restriction
        orga = organization_manager.get_selected_organization(self.request)
        return { field.name: orga.pk }

    def get_queryset(self):
        filters = self.get_restriction_filters()
        queryset = super().get_queryset()
        queryset = queryset.filter(**filters)
        return queryset


class AbstractSaleCreateUpdateMixin(object):
    formset_class = None

    def get_context_data(self, **kwargs):
        assert self.formset_class is not None, "No formset class specified"
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['line_formset'] = (
                self.formset_class(self.request.POST, instance=self.object))
        else:
            context['line_formset'] = (
                self.formset_class(instance=self.object))
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        line_formset = context['line_formset']
        if not line_formset.is_valid():
            return super().form_invalid(form)

        self.object = form.save()
        line_formset.instance = self.object
        line_formset.save()

        # update totals
        self.object.compute_totals()

        return super().form_valid(form)


class AbstractSaleDetailMixin(object):

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (queryset
            .select_related(
                'client',
                'organization'))
        return queryset

    def get_object(self):
        # save some db queries by caching the fetched object
        if hasattr(self, '_object'):
            return getattr(self, '_object')

        obj = super().get_object()
        setattr(self, '_object', obj)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        ctx["checklist"] = obj.full_check()
        ctx["lines"] = (obj.lines.all()
            .select_related(
                'tax_rate')
            .prefetch_related(
                'tax_rate__components'))
        return ctx


class TaxRateCreateUpdateMixin(object):
    formset_class = None

    def get_context_data(self, **kwargs):
        assert self.formset_class is not None, "No formset class specified"
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


class PaymentFormMixin(generic.edit.FormMixin):
    payment_form_class = None

    def get_context_data(self, **kwargs):
        assert self.payment_form_class is not None, "No formset class specified"
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        form = self.get_form(self.payment_form_class)
        context['payment_form'] = form
        return context

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form(self.payment_form_class)
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
