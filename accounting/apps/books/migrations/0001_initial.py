# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import accounting.apps.books.utils
from django.conf import settings
import datetime
import accounting.libs.checks
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('display_name', models.CharField(help_text='Name that you communicate', max_length=150)),
                ('legal_name', models.CharField(help_text='Official name to appear on your reports, sales invoices and bills', max_length=150)),
                ('members', models.ManyToManyField(null=True, blank=True, related_name='organizations', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(related_name='owned_organizations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
