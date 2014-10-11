from django import template
from django.forms import ModelForm
from django.forms.forms import BoundField
from django.template import Context
from django.template.loader import get_template


register = template.Library()


@register.filter
def css_class(field):
    if isinstance(field, BoundField):
        field = field.field
    return field.widget.__class__.__name__.lower()


@register.filter
def is_disabled(field):
    if isinstance(field, BoundField):
        field = field.field
    return 'disabled' in field.widget.attrs


@register.filter
def is_readonly(field):
    if isinstance(field, BoundField):
        field = field.field
    return ('readonly' in field.widget.attrs
        and field.widget.attrs.get('readonly') is True)


@register.filter
def get_form_model_verbose_name(form):
    if not isinstance(form, ModelForm):
        return '<unknown>'
    return form._meta.model._meta.verbose_name.capitalize()
