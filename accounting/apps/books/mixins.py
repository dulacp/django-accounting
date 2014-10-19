from .models import Organization


class SelectedOrganizationMixin(object):
    selected_organization_key = 'selected_organization_pk'

    def set_selected_organization(self, organization):
        key = self.selected_organization_key
        self.request.session[key] = organization.pk

    def get_selected_organization(self):
        key = self.selected_organization_key
        pk = self.request.session[key]
        organization = Organization.objects.get(pk=pk)
        return organization
