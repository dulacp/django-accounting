# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_bill_billline'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billline',
            old_name='unit_price',
            new_name='unit_price_excl_tax',
        ),
        migrations.RenameField(
            model_name='invoiceline',
            old_name='unit_price',
            new_name='unit_price_excl_tax',
        ),
        migrations.AddField(
            model_name='bill',
            name='total_excl_tax',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Order total (excl. tax)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bill',
            name='total_incl_tax',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Order total (inc. tax)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_excl_tax',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Order total (excl. tax)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_incl_tax',
            field=models.DecimalField(default=0, decimal_places=2, max_digits=12, verbose_name='Order total (inc. tax)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bill',
            name='client',
            field=models.ForeignKey(to='people.Client', verbose_name='From Client'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='organization',
            field=models.ForeignKey(to='books.Organization', verbose_name='To Organization'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='organization',
            field=models.ForeignKey(to='books.Organization', verbose_name='From Organization'),
        ),
    ]
