# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0012_auto_20141019_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='total_excl_tax',
            field=models.DecimalField(verbose_name='Total (excl. tax)', max_digits=12, decimal_places=2, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='bill',
            name='total_incl_tax',
            field=models.DecimalField(verbose_name='Total (inc. tax)', max_digits=12, decimal_places=2, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_excl_tax',
            field=models.DecimalField(verbose_name='Total (excl. tax)', max_digits=12, decimal_places=2, default=Decimal('0')),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_incl_tax',
            field=models.DecimalField(verbose_name='Total (inc. tax)', max_digits=12, decimal_places=2, default=Decimal('0')),
        ),
    ]
