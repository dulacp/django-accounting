# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('books', '0009_auto_20141013_0848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('amount', models.DecimalField(max_digits=12, verbose_name='Amount', decimal_places=2)),
                ('detail', models.CharField(max_length=255)),
                ('date_paid', models.DateField(default=datetime.date.today)),
                ('reference', models.CharField(null=True, blank=True, max_length=255)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ('-date_paid',),
            },
            bases=(models.Model,),
        ),
    ]
