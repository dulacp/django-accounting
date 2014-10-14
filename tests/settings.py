import os
import logging

import accounting
from accounting.defaults import *


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = "abcdef"

LANGUAGE_CODE = 'fr-fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.staticfiles',

    'tests._site.model_tests_app',  # contains models we need for testing
) + accounting.get_apps()

# convert INSTALL_APPS to `list`
INSTALLED_APPS = list(INSTALLED_APPS)

# Remove 'debug_toolbar'
try:
    INSTALLED_APPS.remove('debug_toolbar')
except ValueError:
    pass

# Add the 'tests' app, to load test models
INSTALLED_APPS.append('tests')

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'accounting.apps.context_processors.metadata',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

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
    os.path.normpath(os.path.join(BASE_DIR, '../tests/fixtures')),
)
