# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0024_estimateline'),
    ]

    operations = [
        migrations.CreateModel(
            name='FinancialSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('financial_year_end_day', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('financial_year_end_month', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('tax_id_number', models.CharField(max_length=150)),
                ('tax_id_display_name', models.CharField(max_length=150)),
                ('tax_period', models.CharField(max_length=20, choices=[('monthly', '1 month'), ('bimonthly', '2 months'), ('quarter', '3 months'), ('half', '6 months'), ('year', '1 year')], verbose_name='Tax Period')),
                ('organization', models.OneToOneField(blank=True, related_name='financial_settings', null=True, to='books.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
