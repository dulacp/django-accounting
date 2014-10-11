# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import apps.books.utils
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(editable=False, max_length=6, unique=True, default=apps.books.utils.next_invoice_number)),
                ('draft', models.BooleanField(default=False)),
                ('sent', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('date_issued', models.DateField(default=datetime.date.today)),
                ('date_paid', models.DateField(blank=True, null=True)),
                ('organization', models.ForeignKey(to='books.Organization')),
            ],
            options={
                'ordering': ('-date_issued', 'id'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='InvoiceLine',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('unit_price', models.DecimalField(max_digits=8, decimal_places=2)),
                ('quantity', models.DecimalField(max_digits=8, default=1, decimal_places=2)),
                ('invoice', models.ForeignKey(related_name='lines', to='books.Invoice')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='organization',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
