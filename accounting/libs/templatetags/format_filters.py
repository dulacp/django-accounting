import datetime

from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as django_now
from django.utils.translation import to_locale, get_language

from babel.numbers import format_percent

register = template.Library()


@register.filter('percentage')
def percentage_formatter(value):
    if value or value == 0:
        kwargs = {
            'locale': to_locale(get_language()),
            'format': "#,##0.00 %",
        }
        return format_percent(value, **kwargs)


@register.filter
def smartdate(value):
    if isinstance(value, datetime.datetime):
        now = django_now()
    else:
        now = datetime.date.today()

    timedelta = value - now
    format = _(u"%(delta)s %(unit)s")
    delta = abs(timedelta.days)

    if delta > 30:
        delta = int(delta / 30)
        unit = _(u"mois")
    else:
        unit = _(u"jours")

    ctx = {
        'delta': delta,
        'unit': unit,
    }

    return format % ctx
