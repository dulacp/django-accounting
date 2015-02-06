# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0008_auto_20150206_1843'),
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
        migrations.RenameField(
            model_name='bill',
            old_name='number_int',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='estimate',
            old_name='number_int',
            new_name='number',
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='number_int',
            new_name='number',
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='estimate',
            unique_together=set([('number', 'organization')]),
        ),
        migrations.AlterUniqueTogether(
            name='invoice',
            unique_together=set([('number', 'organization')]),
        ),
    ]
