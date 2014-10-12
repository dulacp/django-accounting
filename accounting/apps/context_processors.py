from django.conf import settings


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {
        'display_version': getattr(settings, 'DISPLAY_VERSION', False),
        'version': getattr(settings, 'VERSION', 'N/A'),
    }
