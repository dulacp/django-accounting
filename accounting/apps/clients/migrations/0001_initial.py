# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20141012_0141'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('address_line_1', models.CharField(max_length=128)),
                ('address_line_2', models.CharField(null=True, max_length=128, blank=True)),
                ('city', models.CharField(max_length=64)),
                ('postal_code', models.CharField(max_length=7)),
                ('country', models.CharField(max_length=50)),
                ('organization', models.ForeignKey(null=True, to='books.Organization', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
