from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Organization(models.Model):
    display_name = models.CharField(max_length=150,
        help_text="Name that you communicate")
    legal_name = models.CharField(max_length=150,
        help_text="Official name to appear on your reports, sales "
                  "invoices and bills")

    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True, null=True)
