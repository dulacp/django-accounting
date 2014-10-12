import os
import sys


def configure():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    from django.conf import settings, global_settings

    # Helper function to extract absolute path
    location = lambda x: os.path.join(
        os.path.dirname(os.path.realpath(__file__)), x)

    sys.path.append(location('../accounting'))
