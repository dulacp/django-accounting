# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def migrate_client_data(apps, schema_editor):
    OldClient = apps.get_model("clients", "Client")
    NewClient = apps.get_model("people", "Client")

    for old_client in OldClient.objects.all():
        new_client = NewClient()

        # props
        new_client.name           = old_client.name
        new_client.address_line_1 = old_client.address_line_1
        new_client.address_line_2 = old_client.address_line_2
        new_client.city           = old_client.city
        new_client.postal_code    = old_client.postal_code
        new_client.country        = old_client.country

        # relationship
        new_client.organization   = old_client.organization

        new_client.save()

        # move all related invoices/bills
        def _set_new_client(sales_queryset):
            for sale in sales_queryset:
                sale.new_client = new_client
                sale.save()

        _set_new_client(old_client.estimate_set.all())
        _set_new_client(old_client.invoice_set.all())
        _set_new_client(old_client.bill_set.all())


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(migrate_client_data),
    ]
