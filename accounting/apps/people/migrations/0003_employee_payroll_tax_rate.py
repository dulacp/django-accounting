# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0002_auto_20141029_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='payroll_tax_rate',
            field=models.DecimalField(default=0, decimal_places=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], max_digits=6),
            preserve_default=False,
        ),
    ]
