# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _migrate_sale_numbers(sales):
    for s in sales:
        s.number_int = int(s.number.strip())
        s.save()


def migrate_estimate_numbers(apps, schema_editor):
    Estimate = apps.get_model("books", "Estimate")
    _migrate_sale_numbers(Estimate.objects.all())


def migrate_invoice_numbers(apps, schema_editor):
    Invoice = apps.get_model("books", "Invoice")
    _migrate_sale_numbers(Invoice.objects.all())


def migrate_bill_numbers(apps, schema_editor):
    Bill = apps.get_model("books", "Bill")
    _migrate_sale_numbers(Bill.objects.all())


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20150206_1836'),
    ]

    operations = [
        migrations.RunPython(migrate_estimate_numbers),
        migrations.RunPython(migrate_invoice_numbers),
        migrations.RunPython(migrate_bill_numbers)
    ]
