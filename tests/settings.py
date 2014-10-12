from accounting.settings.dev import *
from os.path import  normpath

import logging


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

# convert INSTALL_APPS to `list`
INSTALLED_APPS = list(INSTALLED_APPS)

# Remove 'debug_toolbar'
try:
    INSTALLED_APPS.remove('debug_toolbar')
except ValueError:
    pass

# Add the 'tests' app, to load test models
INSTALLED_APPS.append('tests')

ADMINS = ('admin@example.com',)
DEBUG = False
TEMPLATE_DEBUG = False
SITE_ID = 1


## Speed up tests

# disable logging
logging.disable(logging.CRITICAL)

# use a cheaper hashing method
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

# Override default fixtures folder
FIXTURE_DIRS = (
    normpath(join(BASE_DIR, '../tests/fixtures')),
)
