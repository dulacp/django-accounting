# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_default_tax_rate(apps, schema_editor):
    # NB: we take for granted that the first tax rate of the organization
    #     is the right one or we create one
    Invoice = apps.get_model("books", "Invoice")
    Bill = apps.get_model("books", "Bill")

    def _set_invoice_or_bill_tax_rate(obj):
        tax_rate, _ = obj.organization.tax_rates.all().get_or_create(
                organization=obj.organization,
                name="No rate defined",
            )
        for line in obj.lines.all():
            line.tax_rate = tax_rate
            line.save()

    for inv in Invoice.objects.all():
        _set_invoice_or_bill_tax_rate(inv)
    for bill in Bill.objects.all():
        _set_invoice_or_bill_tax_rate(bill)


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0019_auto_20141019_2333'),
    ]

    operations = [
        migrations.RunPython(set_default_tax_rate),
    ]
