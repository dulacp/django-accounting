# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0014_auto_20141019_2011'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaxComponent',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('percentage', models.DecimalField(validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], max_digits=6, decimal_places=5)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(verbose_name='Attached to Organization', to='books.Organization', related_name='tax_rates')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='taxcomponent',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate', related_name='components'),
            preserve_default=True,
        ),
    ]
