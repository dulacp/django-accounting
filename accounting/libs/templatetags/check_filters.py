from django import template

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


@register.filter('level_to_css_classname')
def _check_level_to_classname(check):
    """
    Return the appropriated css classname for the check level
    """
    if check.has_failed:
        if check.level == check.LEVEL_ERROR:
            return 'danger'
        elif check.level == check.LEVEL_WARNING:
            return 'warning'
        else:
            return 'info'

    return 'default'


@register.filter('level_to_glyphicon')
def _check_level_to_glyphicon(check):
    """
    Return the appropriated glyph icon for the check level
    """
    if check.has_failed:
        if check.level == check.LEVEL_ERROR:
            return 'minus-sign'
        elif check.level == check.LEVEL_WARNING:
            return 'exclamation-sign'
        else:
            return 'question-sign'

    return 'ok'
