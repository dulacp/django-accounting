# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.contrib.auth import get_user_model


def set_owner(apps, schema_editor):
    # NB: we take for granted that the first user is the superuser
    Organization = apps.get_model("books", "Organization")
    User = get_user_model()
    u = User.objects.all().first()
    for orga in Organization.objects.all():
        orga.owner_id = u.pk
        orga.save()


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0016_organization_owner'),
    ]

    operations = [
        migrations.RunPython(set_owner),
    ]
