# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0027_auto_20141028_1558'),
        ('reports', '0003_payrunsettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessSettings',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('business_type', models.CharField(max_length=50, choices=[('sole_proprietorship', 'Sole Proprietorship')])),
                ('organization', models.OneToOneField(related_name='business_settings', null=True, to='books.Organization', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
