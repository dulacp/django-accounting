from django import template
from django.forms import ModelForm, BaseFormSet
from django.forms.forms import BoundField


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
def get_form_model_verbose_name(instance):
    if isinstance(instance, ModelForm):
        return instance._meta.model._meta.verbose_name.title()
    if isinstance(instance, BaseFormSet):
        return instance.model._meta.verbose_name_plural.title()
    return '<unknown>'
