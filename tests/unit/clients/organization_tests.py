from decimal import Decimal as D

from django.test import TestCase

from django_dynamic_fixture import G

from accounting.apps.books.models import Organization, Invoice, Bill


class TestOrganizationCalcultation(TestCase):

    def setUp(self):
        self.organization = G(Organization)

    def tearDown(self):
        pass

    def test_turnover_excl_tax_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.assertEqual(self.organization.turnover_excl_tax,
            D('10.00') + D('30.00'))

    def test_turnover_incl_tax_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.assertEqual(self.organization.turnover_incl_tax,
            D('12.00') + D('40.00'))

    def test_debts_excl_tax_is_valid(self):
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        bill2 = G(Bill,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        self.organization.bills.add(bill1)
        self.organization.bills.add(bill2)
        self.assertEqual(self.organization.debts_excl_tax,
            D('10.00') + D('30.00'))

    def test_debts_incl_tax_is_valid(self):
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        bill2 = G(Bill,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        self.organization.bills.add(bill1)
        self.organization.bills.add(bill2)
        self.assertEqual(self.organization.debts_incl_tax,
            D('12.00') + D('40.00'))

    def test_profits_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('15.00'),
            total_incl_tax=D('18.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.organization.bills.add(bill1)
        self.assertEqual(self.organization.profits,
            D('10.00') + D('30.00') - D('15.00'))

    def test_collected_tax_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('15.00'),
            total_incl_tax=D('18.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.organization.bills.add(bill1)
        self.assertEqual(self.organization.collected_tax,
            D('2.00') + D('10.00'))

    def test_deductible_tax_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('15.00'),
            total_incl_tax=D('18.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.organization.bills.add(bill1)
        self.assertEqual(self.organization.deductible_tax,
            D('3.00'))

    def test_tax_provisionning_is_valid(self):
        invoice1 = G(Invoice,
            number=101,
            total_excl_tax=D('10.00'),
            total_incl_tax=D('12.00'))
        invoice2 = G(Invoice,
            number=102,
            total_excl_tax=D('30.00'),
            total_incl_tax=D('40.00'))
        bill1 = G(Bill,
            number=101,
            total_excl_tax=D('15.00'),
            total_incl_tax=D('18.00'))
        self.organization.invoices.add(invoice1)
        self.organization.invoices.add(invoice2)
        self.organization.bills.add(bill1)
        self.assertEqual(self.organization.tax_provisionning,
            D('2.00') + D('10.00') - D('3.00'))
