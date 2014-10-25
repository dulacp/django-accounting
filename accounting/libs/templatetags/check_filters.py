import re

from django import template
from django.db.models import Field

from accounting.libs.checks import CheckingModelMixin

register = template.Library()


@register.filter
def check(obj, field_name=None):
    """
    Can check an entire model or just a single model field
    """
    if isinstance(obj, CheckingModelMixin):
        if not field_name:
            check = obj.full_check()
        else:
            check = obj.get_check_for_field(field_name)
    else:
        return None

    return check
