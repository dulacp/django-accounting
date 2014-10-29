# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20141029_1606'),
        ('people', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='client',
            field=models.ForeignKey(to='people.Client', verbose_name='To Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='organization',
            field=models.ForeignKey(related_name='invoices', to='books.Organization', verbose_name='From Organization'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AddField(
            model_name='estimateline',
            name='invoice',
            field=models.ForeignKey(to='books.Estimate', related_name='lines'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estimateline',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estimate',
            name='client',
            field=models.ForeignKey(to='people.Client', verbose_name='To Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='estimate',
            name='organization',
            field=models.ForeignKey(related_name='estimates', to='books.Organization', verbose_name='From Organization'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='estimate',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AddField(
            model_name='billline',
            name='bill',
            field=models.ForeignKey(to='books.Bill', related_name='lines'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='billline',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='client',
            field=models.ForeignKey(to='people.Client', verbose_name='From Client'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bill',
            name='organization',
            field=models.ForeignKey(related_name='bills', to='books.Organization', verbose_name='To Organization'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('number', 'organization')]),
        ),
    ]
