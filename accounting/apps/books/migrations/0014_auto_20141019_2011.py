# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.apps.books.utils


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0013_auto_20141019_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='number',
            field=models.CharField(default=accounting.apps.books.utils.next_invoice_number, max_length=6),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(default=accounting.apps.books.utils.next_invoice_number, max_length=6),
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('number', 'organization')]),
        ),
    ]
