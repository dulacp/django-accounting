from django.db.models.fields import FieldDoesNotExist

from .models import Organization


class SelectedOrganizationMixin(object):
    selected_organization_key = 'selected_organization_pk'

    def set_selected_organization(self, organization):
        key = self.selected_organization_key
        self.request.session[key] = organization.pk

    def get_selected_organization(self):
        key = self.selected_organization_key
        if key not in self.request.session:
            return

        pk = self.request.session[key]
        organization = Organization.objects.get(pk=pk)
        return organization


class RestrictToSelectedOrganizationQuerySetMixin(object):
    """
    To restrict objects to the current selected organization

    NB: use in conjonction with `SelectedOrganizationMixin`
    """

    def get_restriction_filters(self):
        # check for the field
        meta = self.model._meta
        field, model, direct, m2m = meta.get_field_by_name('organization')

        # build the restriction
        organization = self.get_selected_organization()
        return { field.name: organization.pk }

    def get_queryset(self):
        filters = self.get_restriction_filters()
        queryset = super().get_queryset()
        queryset = queryset.filter(**filters)
        return queryset
