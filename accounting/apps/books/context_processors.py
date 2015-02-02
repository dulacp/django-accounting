from .utils import organization_manager
from .models import Organization


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
        user_organizations = request.user.organizations.all()

    return {
        'user_organizations': user_organizations,
        'selected_organization': orga,
    }
