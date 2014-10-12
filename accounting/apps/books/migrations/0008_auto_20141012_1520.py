# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20141012_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='organization',
            field=models.ForeignKey(verbose_name='To Organization', related_name='bills', to='books.Organization'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='total_excl_tax',
            field=models.DecimalField(verbose_name='Total (excl. tax)', decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='bill',
            name='total_incl_tax',
            field=models.DecimalField(verbose_name='Total (inc. tax)', decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='organization',
            field=models.ForeignKey(verbose_name='From Organization', related_name='invoices', to='books.Organization'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_excl_tax',
            field=models.DecimalField(verbose_name='Total (excl. tax)', decimal_places=2, max_digits=12),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='total_incl_tax',
            field=models.DecimalField(verbose_name='Total (inc. tax)', decimal_places=2, max_digits=12),
        ),
    ]
