from django.test import TestCase
from django.db import models
from django.db.models.query import QuerySet
from django.conf import settings

from accounting.libs.fields import UUIDField


class MockModelWitNoFields(models.Model):
    """No fields"""
    pass


class MockModelWithUUIDField(models.Model):
    dymmy = models.CharField(max_length=254)
    uid = UUIDField(blank=True)
