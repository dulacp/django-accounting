# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('books', '0027_auto_20141028_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='new_client',
            field=models.ForeignKey(blank=True, verbose_name='From Client', to='people.Client', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estimate',
            name='new_client',
            field=models.ForeignKey(blank=True, verbose_name='To Client', to='people.Client', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='new_client',
            field=models.ForeignKey(blank=True, verbose_name='To Client', to='people.Client', null=True),
            preserve_default=True,
        ),
    ]
