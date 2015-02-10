# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20150206_1850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill',
            name='draft',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='sent',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='draft',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='sent',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='draft',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='paid',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='sent',
        ),
    ]
