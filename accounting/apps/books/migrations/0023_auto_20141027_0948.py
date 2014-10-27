# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import accounting.apps.books.utils
import datetime
import accounting.libs.checks


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('books', '0022_auto_20141025_1102'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estimate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('number', models.CharField(max_length=6, default=accounting.apps.books.utils.next_invoice_number)),
                ('total_incl_tax', models.DecimalField(default=Decimal('0'), verbose_name='Total (inc. tax)', max_digits=12, decimal_places=2)),
                ('total_excl_tax', models.DecimalField(default=Decimal('0'), verbose_name='Total (excl. tax)', max_digits=12, decimal_places=2)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_dued', models.DateField(blank=True, null=True, verbose_name='Due date', help_text='The date when the total amount should have been collected')),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(verbose_name='To Client', to='clients.Client')),
                ('organization', models.ForeignKey(related_name='estimates', verbose_name='From Organization', to='books.Organization')),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(accounting.libs.checks.CheckingModelMixin, models.Model),
        ),
        migrations.AlterUniqueTogether(
            name='estimate',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AlterField(
            model_name='bill',
            name='date_dued',
            field=models.DateField(blank=True, null=True, verbose_name='Due date', help_text='The date when the total amount should have been collected'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='date_dued',
            field=models.DateField(blank=True, null=True, verbose_name='Due date', help_text='The date when the total amount should have been collected'),
        ),
    ]
