# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0023_auto_20141027_0948'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstimateLine',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('description', models.TextField(null=True, blank=True)),
                ('unit_price_excl_tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('quantity', models.DecimalField(default=1, decimal_places=2, max_digits=8)),
                ('invoice', models.ForeignKey(to='books.Estimate', related_name='lines')),
                ('tax_rate', models.ForeignKey(to='books.TaxRate')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
