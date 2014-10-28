# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_estimateline'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxrate',
            name='rate',
            field=models.DecimalField(decimal_places=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], default=0, max_digits=6),
            preserve_default=False,
        ),
    ]
