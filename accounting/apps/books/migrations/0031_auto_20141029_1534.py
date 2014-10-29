# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0030_auto_20141029_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='new_client',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='new_client',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='new_client',
        ),
    ]
