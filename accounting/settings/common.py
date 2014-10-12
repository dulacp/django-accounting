"""
Django settings for accounting project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

import os
import sys
from decimal import Decimal

import accounting


VERSION = accounting.VERSION
DISPLAY_VERSION = accounting.get_version()
DISPLAY_SHORT_VERSION = accounting.get_short_version()


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.basename(BASE_DIR)

# Add the BASE_DIR to the path in order to reuse the apps easily
sys.path.append(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'o7k)j*lewj6va4yqz=#1^z@6wtf!$#dx(u=z!3(351rc27c9fm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'djangobower',
    'bootstrap3',

    'libs',
    'apps.clients',
    'apps.books',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'accounting.urls'

WSGI_APPLICATION = 'accounting.wsgi.application'


# Templates
# https://docs.djangoproject.com/en/1.7/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',

    'apps.context_processors.metadata',
)

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/1.7/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': ''
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# See: https://docs.djangoproject.com/en/1.7/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",

    "djangobower.finders.BowerFinder",
)


# Media files

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Bower config

BOWER_COMPONENTS_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'components'))

BOWER_INSTALLED_APPS = (
    'modernizr',
    'jquery',
    'bootstrap',
)


# User

AUTH_USER_MODEL = 'books.User'


# Accounting

DEFAULT_CURRENCY = "EUR"
DEFAULT_TAX_PERCENTAGE = Decimal("0.20")
