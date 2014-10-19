# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0017_auto_20141019_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(related_name='owned_organizations', to=settings.AUTH_USER_MODEL),
        ),
    ]
