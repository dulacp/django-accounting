import os

# Use 'final' as the 4th element to indicate
# a full release

VERSION = (0, 1, 0, 'alpha', 1)


def get_short_version():
    return '%s.%s' % (VERSION[0], VERSION[1])


def get_version():
    version = '%s.%s' % (VERSION[0], VERSION[1])
    # Append 3rd digit if > 0
    if VERSION[2]:
        version = '%s.%s' % (version, VERSION[2])
    elif VERSION[3] != 'final':
        version = '%s %s' % (version, VERSION[3])
        if len(VERSION) == 5:
            version = '%s %s' % (version, VERSION[4])
    return version


# Cheeky setting that allows each template to be accessible by two paths.
# Eg: the template 'accounting/templates/accounting/base.html' can be accessed
# via both 'base.html' and 'accounting/base.html'.  This allows Accounting's
# templates to be extended by templates with the same filename
ACCOUNTING_MAIN_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'templates/accounting')


ACCOUNTING_APPS = (
    'accounting',
    'accounting.libs',
    'accounting.apps.connect',
    'accounting.apps.people',
    'accounting.apps.books',
    'accounting.apps.reports',

    # Third party apps that accounting depends on
    'bootstrap3',
)


ACCOUNTING_MIDDLEWARE_CLASSES = (
    'accounting.apps.context_processors.metadata',
    'accounting.apps.books.context_processors.organizations',
)


def get_apps():
    return ACCOUNTING_APPS
