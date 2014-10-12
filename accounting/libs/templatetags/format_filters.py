# encoding: utf-8

import json
import datetime

from django import template
from django.template.defaultfilters import floatformat
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as django_now

register = template.Library()


@register.filter
def percentage(value):
    if value or value == 0:
        return "%s %%" % floatformat(value * 100.0, 2)


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
