from .utils import organization_manager


class AutoSelectOrganizationMiddleware(object):

    def process_request(self, request):
        if not request.user or not request.user.is_authenticated():
            return

        orga = organization_manager.get_selected_organization(request)
        if orga is not None:
            return

        user_orgas = organization_manager.get_user_organizations(request.user)
        if user_orgas.count():
            orga = user_orgas.first()
            organization_manager.set_selected_organization(request, orga)
