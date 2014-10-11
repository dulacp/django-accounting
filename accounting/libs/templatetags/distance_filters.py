from django import template

from django.contrib.gis.measure import Distance

register = template.Library()


@register.filter
def has_distance(search_object):
    return bool(search_object._point_of_origin)


@register.filter
def distance(dist):
    if isinstance(dist, Distance):
        d = dist.m
        unit = "m"

        if d > 1000:
            d = dist.km
            unit = "km"

        ctx = {
            'distance': float('%.2g' % d),
            'unit': unit,
        }
        return u"%(distance)s %(unit)s" % ctx
