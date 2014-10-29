# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('address_line_1', models.CharField(max_length=128)),
                ('address_line_2', models.CharField(null=True, max_length=128, blank=True)),
                ('city', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(related_name='orgas', null=True, blank=True, to='books.Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254)),
                ('salaries_follow_profits', models.BooleanField(default=False)),
                ('shares_percentage', models.DecimalField(validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], decimal_places=5, max_digits=6)),
                ('organization', models.ForeignKey(to='books.Organization', related_name='employees')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
