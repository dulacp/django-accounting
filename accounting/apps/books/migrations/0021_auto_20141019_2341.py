# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0020_auto_20141019_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billline',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate'),
        ),
        migrations.AlterField(
            model_name='invoiceline',
            name='tax_rate',
            field=models.ForeignKey(to='books.TaxRate'),
        ),
    ]
