# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('books', '0015_auto_20141019_2128'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, related_name='owned_organizations'),
            preserve_default=True,
        ),
    ]
