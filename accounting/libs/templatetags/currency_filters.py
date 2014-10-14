# encoding: utf-8

from decimal import Decimal as D, InvalidOperation

from django import template
from django.conf import settings
from django.utils.translation import to_locale, get_language

from babel.numbers import format_currency

register = template.Library()


@register.filter(name='currency')
def currency_formatter(value, currency=None):
    """
    Format decimal value as currency
    """
    try:
        value = D(value)
    except (TypeError, InvalidOperation):
        return ""
    # Using Babel's currency formatting
    # http://babel.pocoo.org/docs/api/numbers/#babel.numbers.format_currency
    currency = currency or settings.ACCOUNTING_DEFAULT_CURRENCY
    kwargs = {
        'currency': currency,
        'format': getattr(settings, 'CURRENCY_FORMAT', None),
        'locale': to_locale(get_language()),
    }
    return format_currency(value, **kwargs)
