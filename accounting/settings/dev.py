import os

from .common import *


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar.apps.DebugToolbarConfig',
    )
