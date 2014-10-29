# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def _link_to_first_organization(apps, schema_editor):
    Client = apps.get_model("people", "Client")
    Client.objects.update(organization_id=1)


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0003_employee_payroll_tax_rate'),
    ]

    operations = [
        migrations.RunPython(_link_to_first_organization)
    ]
