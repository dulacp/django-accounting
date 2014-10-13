# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.apps.books.utils


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20141011_1549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='number',
            field=models.CharField(default=accounting.apps.books.utils.next_invoice_number, max_length=6, unique=True),
        ),
    ]
