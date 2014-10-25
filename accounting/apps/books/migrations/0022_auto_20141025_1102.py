# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0021_auto_20141019_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date_dued',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_dued',
            field=models.DateField(blank=True, null=True),
        ),
    ]
