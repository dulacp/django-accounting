# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='financialsettings',
            name='tax_id_display_name',
            field=models.CharField(max_length=150, blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='financialsettings',
            name='tax_id_number',
            field=models.CharField(max_length=150, blank=True, null=True),
        ),
    ]
