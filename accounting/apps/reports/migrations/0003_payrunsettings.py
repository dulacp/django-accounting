# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0027_auto_20141028_1558'),
        ('reports', '0002_auto_20141027_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayRunSettings',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('salaries_follow_profits', models.BooleanField(default=False)),
                ('payrun_period', models.CharField(default='monthly', verbose_name='Payrun Period', choices=[('monthly', 'monthly')], max_length=20)),
                ('organization', models.OneToOneField(to='books.Organization', blank=True, related_name='payrun_settings', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
