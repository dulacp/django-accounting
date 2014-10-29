# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20141029_1606'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address_line_1', models.CharField(max_length=128)),
                ('address_line_2', models.CharField(null=True, blank=True, max_length=128)),
                ('city', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(null=True, related_name='orgas', to='books.Organization', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('salaries_follow_profits', models.BooleanField(default=False)),
                ('shares_percentage', models.DecimalField(decimal_places=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], max_digits=6)),
                ('organization', models.ForeignKey(to='books.Organization', related_name='employees')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
