# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20141029_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('business_type', models.CharField(choices=[('sole_proprietorship', 'Sole Proprietorship')], max_length=50)),
                ('organization', models.OneToOneField(related_name='business_settings', to='books.Organization', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinancialSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('financial_year_end_day', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(31)])),
                ('financial_year_end_month', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)])),
                ('tax_id_number', models.CharField(null=True, blank=True, max_length=150)),
                ('tax_id_display_name', models.CharField(null=True, blank=True, max_length=150)),
                ('tax_period', models.CharField(verbose_name='Tax Period', choices=[('monthly', '1 month'), ('bimonthly', '2 months'), ('quarter', '3 months'), ('half', '6 months'), ('year', '1 year')], max_length=20)),
                ('organization', models.OneToOneField(related_name='financial_settings', to='books.Organization', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PayRunSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('salaries_follow_profits', models.BooleanField(default=False)),
                ('payrun_period', models.CharField(verbose_name='Payrun Period', default='monthly', choices=[('monthly', 'monthly')], max_length=20)),
                ('organization', models.OneToOneField(related_name='payrun_settings', to='books.Organization', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
