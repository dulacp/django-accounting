# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import accounting.apps.books.utils
from decimal import Decimal
import datetime
import accounting.libs.checks


def next_invoice_number():
    return 100


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(default=next_invoice_number, max_length=6)),
                ('total_incl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (inc. tax)', max_digits=12)),
                ('total_excl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (excl. tax)', max_digits=12)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_dued', models.DateField(null=True, help_text='The date when the total amount should have been collected', verbose_name='Due date', blank=True)),
                ('date_paid', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(accounting.libs.checks.CheckingModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='BillLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('unit_price_excl_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(default=next_invoice_number, max_length=6)),
                ('total_incl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (inc. tax)', max_digits=12)),
                ('total_excl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (excl. tax)', max_digits=12)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_dued', models.DateField(null=True, help_text='The date when the total amount should have been collected', verbose_name='Due date', blank=True)),
                ('date_paid', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(accounting.libs.checks.CheckingModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='EstimateLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('unit_price_excl_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(default=next_invoice_number, max_length=6)),
                ('total_incl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (inc. tax)', max_digits=12)),
                ('total_excl_tax', models.DecimalField(decimal_places=2, default=Decimal('0'), verbose_name='Total (excl. tax)', max_digits=12)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_dued', models.DateField(null=True, help_text='The date when the total amount should have been collected', verbose_name='Due date', blank=True)),
                ('date_paid', models.DateField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(accounting.libs.checks.CheckingModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('unit_price_excl_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('invoice', models.ForeignKey(to='books.Invoice', related_name='lines')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(decimal_places=2, verbose_name='Amount', max_digits=12)),
                ('detail', models.CharField(null=True, blank=True, max_length=255)),
                ('date_paid', models.DateField(default=datetime.date.today)),
                ('reference', models.CharField(null=True, blank=True, max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-date_paid',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('rate', models.DecimalField(decimal_places=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('1'))], max_digits=6)),
                ('organization', models.ForeignKey(related_name='tax_rates', to='books.Organization', verbose_name='Attached to Organization')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate'),
            preserve_default=True,
        ),
    ]
