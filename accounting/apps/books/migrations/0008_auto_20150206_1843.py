# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20150206_1836'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bill',
            options={'ordering': ('-number_int',)},
        ),
        migrations.AlterModelOptions(
            name='estimate',
            options={'ordering': ('-number_int',)},
        ),
        migrations.AlterModelOptions(
            name='invoice',
            options={'ordering': ('-number_int',)},
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('number_int', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='bill',
            name='number',
        ),
        migrations.AlterUniqueTogether(
            name='estimate',
            unique_together=set([('number_int', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='estimate',
            name='number',
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('number_int', 'organization')]),
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='number',
        ),
    ]
