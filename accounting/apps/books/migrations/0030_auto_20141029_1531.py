# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def move_new_client_to_client(apps, schema_editor):
    Estimate = apps.get_model("books", "Estimate")
    Invoice = apps.get_model("books", "Invoice")
    Bill = apps.get_model("books", "Bill")

    # move all related invoices/bills
    def _set_new_client(sales_queryset):
        for sale in sales_queryset:
            sale.client_id = sale.new_client_id or 0
            sale.save()

    _set_new_client(Estimate.objects.all())
    _set_new_client(Invoice.objects.all())
    _set_new_client(Bill.objects.all())


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0029_auto_20141029_1531'),
    ]

    operations = [
        migrations.RunPython(move_new_client_to_client)
    ]
