# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0018_auto_20141019_2150'),
    ]

    operations = [
        migrations.AddField(
            model_name='billline',
            name='tax_rate',
            field=models.ForeignKey(null=True, blank=True, to='books.TaxRate'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoiceline',
            name='tax_rate',
            field=models.ForeignKey(null=True, blank=True, to='books.TaxRate'),
            preserve_default=True,
        ),
    ]
