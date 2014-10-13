from decimal import Decimal as D

from django.test import TestCase

from django_dynamic_fixture import G
import mock

from accounting.apps.books.models import Invoice


class TestInvoiceQuerySetMethods(TestCase):

    def setUp(self):
        pass

    def test_returns_correct_turnovers(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))

        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('5.00'),
            total_incl_tax=D('6.00'))

        queryset = Invoice.objects.all()
        self.assertEqual(queryset.turnover_excl_tax(), D('10.00') + D('5.00'))
        self.assertEqual(queryset.turnover_incl_tax(), D('12.00') + D('6.00'))
