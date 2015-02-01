# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_auto_20150128_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businesssettings',
            name='business_type',
            field=models.CharField(choices=[('sole_proprietorship', 'Sole Proprietorship'), ('partnership', 'Partnership'), ('corporation', 'Corporation')], max_length=50),
            preserve_default=True,
        ),
    ]
