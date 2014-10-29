# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0028_auto_20141029_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='client',
            field=models.ForeignKey(verbose_name='From Client', to='people.Client'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='new_client',
            field=models.ForeignKey(verbose_name='From Client', blank=True, to='people.Client', related_name='+', null=True),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='client',
            field=models.ForeignKey(verbose_name='To Client', to='people.Client'),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='new_client',
            field=models.ForeignKey(verbose_name='To Client', blank=True, to='people.Client', related_name='+', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(verbose_name='To Client', to='people.Client'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='new_client',
            field=models.ForeignKey(verbose_name='To Client', blank=True, to='people.Client', related_name='+', null=True),
        ),
    ]
