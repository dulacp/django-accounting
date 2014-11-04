# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.apps.books.utils


def next_invoice_number():
    return 100


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20141029_1606'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ('-number',)},
        ),
        migrations.AlterModelOptions(
            name='estimate',
            options={'ordering': ('-number',)},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-number',)},
        ),
        migrations.AlterField(
            model_name='bill',
            name='number',
            field=models.CharField(max_length=6, db_index=True, default=next_invoice_number),
        ),
        migrations.AlterField(
            model_name='estimate',
            name='number',
            field=models.CharField(max_length=6, db_index=True, default=next_invoice_number),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(max_length=6, db_index=True, default=next_invoice_number),
        ),
    ]
