from django.conf import settings


def metadata(request):
    """
    Add some generally useful metadata to the template context
    """
    return {
        'display_version': getattr(settings,
            'DISPLAY_VERSION', 'N/A'),
        'display_short_version': getattr(settings,
            'DISPLAY_SHORT_VERSION', 'N/A'),
        'version': getattr(settings,
            'VERSION', 'N/A'),
    }
