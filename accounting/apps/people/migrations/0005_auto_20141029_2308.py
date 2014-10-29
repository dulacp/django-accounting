# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_auto_20141029_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='organization',
            field=models.ForeignKey(related_name='clients', to='books.Organization'),
        ),
    ]
