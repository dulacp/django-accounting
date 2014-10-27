class OrganizationManager(object):
    selected_organization_key = 'selected_organization_pk'

    def set_selected_organization(self, request, organization):
        key = self.selected_organization_key
        request.session[key] = organization.pk

    def get_selected_organization(self, request):
        key = self.selected_organization_key
        if key not in request.session:
            return

        # To avoid circular imports
        from .models import Organization

        pk = request.session[key]
        organization = Organization.objects.get(pk=pk)
        return organization


organization_manager = OrganizationManager()


# TODO implement nicely this feature
def next_invoice_number():
    return 100
