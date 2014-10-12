from django import template

register = template.Library()


@register.filter(name='times')
def times(number):
    return range(number)


@register.filter
def get_object(l, index):
    return l[index]


@register.filter
def get_item(d, key, default=None):
    if default:
        d.get(key, None)
    return d.get(key)
