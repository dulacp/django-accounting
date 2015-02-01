from .utils import organization_manager
from .models import Organization


def organizations(request):
    """
    Add some generally useful metadata to the template context
    """
    orga = organization_manager.get_selected_organization(request)
    return {
        'all_organizations': Organization.objects.all(),
        'selected_organization': orga,
    }
