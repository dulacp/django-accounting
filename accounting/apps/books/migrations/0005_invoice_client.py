# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('books', '0004_auto_20141012_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(verbose_name='To Client', default=0, to='clients.Client'),
            preserve_default=False,
        ),
    ]
