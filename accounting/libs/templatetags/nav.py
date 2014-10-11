# encoding: utf-8

import re

from django import template
register = template.Library()


@register.simple_tag
def active(request, pattern):
    if hasattr(request, 'path') and re.search(pattern, request.path):
        return 'active'
    return ''
