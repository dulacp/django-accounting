from decimal import Decimal as D

from django.test import TestCase

import mock

# from apps.books import calculators
# from libs import prices
# TODO steal the above from django-oscar
# https://github.com/tangentlabs/django-oscar/blob/master/oscar/core/prices.py


class TestInvoiceTotalCalculation(TestCase):

    def setUp(self):
        pass

    # def test_returns_correct_totals_when_tax_is_known(self):
    #     basket = mock.Mock()
    #     basket.total_excl_tax = D('10.00')
    #     basket.total_incl_tax = D('12.00')
    #     basket.is_tax_known = True

    #     shipping_charge = prices.Price(
    #         currency=basket.currency, excl_tax=D('5.00'),
    #         tax=D('0.50'))

    #     total = self.calculator.calculate(basket, shipping_charge)

    #     self.assertIsInstance(total, prices.Price)
    #     self.assertEqual(D('10.00') + D('5.00'), total.excl_tax)
    #     self.assertTrue(total.is_tax_known)
    #     self.assertEqual(D('12.00') + D('5.50'), total.incl_tax)
    #     self.assertEqual(D('2.00') + D('0.50'), total.tax)
