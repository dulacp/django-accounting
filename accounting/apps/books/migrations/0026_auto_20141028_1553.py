# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from decimal import Decimal as D
from django.db import models, migrations


def set_tax_rates(apps, schema_editor):
    TaxRate = apps.get_model("books", "TaxRate")

    for tax in TaxRate.objects.all():
        r = D('0.000')
        for c in tax.components.all():
            r += c.percentage
        tax.rate = r
        tax.save()


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0025_taxrate_rate'),
    ]

    operations = [
        migrations.RunPython(set_tax_rates),
    ]
