# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20141104_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='number',
            field=models.CharField(default=1, max_length=6, db_index=True),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='number',
            field=models.CharField(default=1, max_length=6, db_index=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(default=1, max_length=6, db_index=True),
        ),
    ]
