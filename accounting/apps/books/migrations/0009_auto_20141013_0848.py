# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20141012_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='date_dued',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='date_dued',
            field=models.DateField(default=datetime.date(2014, 10, 13)),
            preserve_default=False,
        ),
    ]
