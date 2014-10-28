# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0026_auto_20141028_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxcomponent',
            name='tax_rate',
        ),
        migrations.DeleteModel(
            name='TaxComponent',
        ),
    ]
