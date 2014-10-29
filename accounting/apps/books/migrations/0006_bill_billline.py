# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import accounting.apps.books.utils


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0001_initial'),
        ('books', '0005_invoice_client'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('number', models.CharField(default=accounting.apps.books.utils.next_invoice_number, unique=True, max_length=6)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('client', models.ForeignKey(verbose_name='To Client', to='people.Client')),
                ('organization', models.ForeignKey(to='books.Organization')),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BillLine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(decimal_places=2, default=1, max_digits=8)),
                ('bill', models.ForeignKey(to='books.Bill', related_name='lines')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
