# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20150128_1458'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='number_int',
            field=models.IntegerField(default=1, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estimate',
            name='number_int',
            field=models.IntegerField(default=1, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='number_int',
            field=models.IntegerField(default=1, db_index=True),
            preserve_default=True,
        ),
    ]
