from django.db.models import Q

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
        user = request.user
        user_organizations = (Organization.objects
            .filter(Q(members=user) | Q(owner=user)))

    return {
        'user_organizations': user_organizations,
        'selected_organization': orga,
    }
