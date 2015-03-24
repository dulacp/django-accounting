# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal
import datetime
import accounting.libs.checks


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20141029_2308'),
        ('books', '0010_auto_20150210_1449'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseClaim',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(db_index=True, default=1)),
                ('total_incl_tax', models.DecimalField(verbose_name='Total (inc. tax)', max_digits=12, default=Decimal('0'), decimal_places=2)),
                ('total_excl_tax', models.DecimalField(verbose_name='Total (excl. tax)', max_digits=12, default=Decimal('0'), decimal_places=2)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_dued', models.DateField(verbose_name='Due date', blank=True, null=True, help_text='The date when the total amount should have been collected')),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('employee', models.ForeignKey(verbose_name='Paid by employee', to='people.Employee')),
                ('organization', models.ForeignKey(related_name='expense_claims', to='books.Organization', verbose_name='From Organization')),
            ],
            options={
                'ordering': ('-number',),
            },
            bases=(accounting.libs.checks.CheckingModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ExpenseClaimLine',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price_excl_tax', models.DecimalField(max_digits=8, decimal_places=2)),
                ('quantity', models.DecimalField(max_digits=8, default=1, decimal_places=2)),
                ('expense_claim', models.ForeignKey(related_name='lines', to='books.ExpenseClaim')),
                ('tax_rate', models.ForeignKey(to='books.TaxRate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='expenseclaim',
            unique_together=set([('number', 'organization')]),
        ),
    ]
