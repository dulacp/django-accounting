from .utils import organization_manager


def organizations(request):
    """
    Add some generally useful metadata to the template context
    """
    # selected organization
    orga = organization_manager.get_selected_organization(request)

    # all user authorized organizations
    if not request.user or not request.user.is_authenticated():
        user_organizations = None
    else:
        user = request.user
        user_organizations = organization_manager.get_user_organizations(user)

    return {
        'user_organizations': user_organizations,
        'selected_organization': orga,
    }
