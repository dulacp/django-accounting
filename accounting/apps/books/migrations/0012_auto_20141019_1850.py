# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0011_auto_20141014_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='detail',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
    ]
