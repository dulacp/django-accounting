from decimal import Decimal as D

from django.test import TestCase
from django.test.client import RequestFactory
from django.template import Template, Context, RequestContext
from django.contrib.auth.models import AnonymousUser
from django import forms

from accounting.libs.templatetags.form_filters import is_disabled, is_readonly


class TestGetParameterTemplateTag(TestCase):

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/', {'page': 3, 'sort': 'asc'})
        self.request.user = AnonymousUser()
        # Simulate that we get throught the middleware
        self.request.franchise = None

    def test_retrieve_get_param(self):
        out = Template(
            "{% load url_tags %}"
            "{% get_parameters %}"
        ).render(RequestContext(self.request, {}))
        self.assertTrue(out == "page=3&sort=asc" or out == "sort=asc&page=3")

    def test_except_fields(self):
        out = Template(
            "{% load url_tags %}"
            "{% get_parameters 'sort' %}"
        ).render(RequestContext(self.request, {}))
        self.assertEqual(out, "page=3")


class TestFormFilterCssClass(TestCase):

    def setUp(self):
        class MockForm(forms.Form):
            text_field = forms.CharField()
            date_field = forms.DateField()
        self.form_class = MockForm
        self.form = self.form_class()

    def test_text_field_class_name(self):
        out = Template(
            "{% load form_filters %}"
            "{% for field in form %}"
            "{{ field|css_class }},"
            "{% endfor %}"
        ).render(Context({
            'form': self.form
        }))
        self.assertEqual(out, "textinput,dateinput,")


class TestFormFilterIsDisable(TestCase):

    def setUp(self):
        class MockForm(forms.Form):
            enabled_field = forms.CharField()
            disabled_field = forms.CharField(
                widget=forms.TextInput(attrs={'disabled': True}))
        self.form_class = MockForm
        self.form = self.form_class()

    def test_return_true_for_disable_fields(self):
        self.assertFalse(is_disabled(self.form.fields['enabled_field']))
        self.assertTrue(is_disabled(self.form.fields['disabled_field']))

    def test_return_true_for_disable_bounded_fields(self):
        """
        Bounded fields are used when we iterate directly through
        a form instance
        """
        bounded_fields = dict((f.name, f) for f in self.form)
        self.assertFalse(is_disabled(bounded_fields['enabled_field']))
        self.assertTrue(is_disabled(bounded_fields['disabled_field']))


class TestFormFilterIsReadonly(TestCase):

    def setUp(self):
        class MockForm(forms.Form):
            writable_field = forms.CharField()
            readonly_field = forms.CharField(
                widget=forms.TextInput(attrs={'readonly': True}))
        self.form_class = MockForm
        self.form = self.form_class()

    def test_return_true_for_readonly_fields(self):
        self.assertFalse(is_readonly(self.form.fields['writable_field']))
        self.assertTrue(is_readonly(self.form.fields['readonly_field']))

    def test_return_true_for_readonly_bounded_fields(self):
        """
        Bounded fields are used when we iterate directly through
        a form instance
        """
        bounded_fields = dict((f.name, f) for f in self.form)
        self.assertFalse(is_readonly(bounded_fields['writable_field']))
        self.assertTrue(is_readonly(bounded_fields['readonly_field']))


class TestMyFilterTimes(TestCase):

    def test_simple_times_filter_loop(self):
        out = Template(
            "{% load my_filters %}"
            "{% for i in 5|times %}"
            "{{ i }},"
            "{% endfor %}"
        ).render(Context())
        self.assertEqual(out, "0,1,2,3,4,")


class TestMyFilterGetItem(TestCase):

    def test_wrong_type_should_raise_exception(self):
        with self.assertRaises(AttributeError):
            Template(
                "{% load my_filters %}"
                "{{ d|get_item:'foo' }}"
            ).render(Context({
                'd': list(range(3)),
            }))

    def test_simple_dict_value_for_key(self):
        out = Template(
            "{% load my_filters %}"
            "{{ d|get_item:'foo' }}"
        ).render(Context({
            'd': dict(foo="bar"),
        }))
        self.assertEqual(out, "bar")


class TestMyFilterGetObject(TestCase):

    def test_simple_list_value_for_index(self):
        out = Template(
            "{% load my_filters %}"
            "{{ list|get_object:1 }}"
        ).render(Context({
            'list': list(range(3)),
        }))
        self.assertEqual(out, "1")


class TestFormatFilterPercentage(TestCase):

    def test_basic_value(self):
        out = Template(
            "{% load format_filters %}"
            "{{ f|percentage }}"
        ).render(Context({
            'f': 0.2345678
        }))
        self.assertEqual(out, "23,46 %")

    def test_zero_value(self):
        out = Template(
            "{% load format_filters %}"
            "{{ f|percentage }}"
        ).render(Context({
            'f': 0
        }))
        self.assertEqual(out, "0,00 %")


class TestUrlTagQuery(TestCase):

    def test_no_parameter_raises_exception(self):
        from classytags.exceptions import ArgumentRequiredError
        with self.assertRaises(ArgumentRequiredError):
            out = Template(
                "{% load url_tags %}"
                "{% query %}"
            ).render(Context({}))

    def test_multiple_parameters(self):
        out = Template(
            "{% load url_tags %}"
            "{% query a=1 b=2 %}"
        ).render(Context({}))
        self.assertTrue(out == "a=1&b=2" or out == "b=2&a=1")

    def test_url_encode_spaces(self):
        out = Template(
            "{% load url_tags %}"
            "{% query q='I got some spaces' %}"
        ).render(Context({}))
        self.assertEqual(out, "q=I+got+some+spaces")


class TestCurrencyFilter(TestCase):

    def setUp(self):
        self.template = Template(
            "{% load currency_filters %}"
            "{{ price|currency }}"
        )

    def test_renders_price_correctly(self):
        out = self.template.render(Context({
            'price': D('10.23'),
        }))
        # remove spaces (from comparision sake)
        out = out.replace("\xa0", '').replace(' ', '')
        self.assertEqual(out, '10,23€')

    def test_handles_none_price_gracefully(self):
        self.template.render(Context({
            'price': None
        }))

    def test_handles_string_price_gracefully(self):
        self.template.render(Context({
            'price': ''
        }))
