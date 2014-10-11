from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class User(AbstractUser):
    objects = UserManager()


class Organization(models.Model):
    display_name = models.CharField(max_length=150,
        help_text="Name that you communicate")
    legal_name = models.CharField(max_length=150,
        help_text="Official name to appear on your reports, sales "
                  "invoices and bills")

    members = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     blank=True, null=True)

    class Meta:
        pass

    def __str__(self):
        return self.legal_name
