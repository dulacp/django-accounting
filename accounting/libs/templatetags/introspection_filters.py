from django import template
from django.forms import ModelForm, BaseFormSet
from django.db.models import Model

from django_select2.fields import (
    AutoModelSelect2Field,
    AutoModelSelect2MultipleField)


register = template.Library()


@register.filter
def get_model_verbose_name(instance):
    if isinstance(instance, Model):
        return instance._meta.verbose_name.title()
    return '<unknown>'


@register.filter
def get_form_model_verbose_name(instance):
    if isinstance(instance, ModelForm):
        return instance._meta.model._meta.verbose_name.title()
    if isinstance(instance, BaseFormSet):
        return instance.model._meta.verbose_name_plural.title()
    return '<unknown>'


@register.filter
def is_select2_field(form, field):
    select2_classes = (AutoModelSelect2Field, AutoModelSelect2MultipleField)
    res = any(isinstance(field.field, cls) for cls in select2_classes)
    return res
