from .utils import organization_manager


def organizations(request):
    """
    Add some generally useful metadata to the template context
    """
    orga = organization_manager.get_selected_organization(request)
    return {
        'selected_organization': orga
    }
