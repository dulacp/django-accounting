from django.template import Library
from django.utils.numberformat import format

register = Library()


@register.filter(name="float_dot")
def do_float_dot(value, decimal_pos=4):
    return format(value or 0, ".", decimal_pos)


do_float_dot.is_safe = True
