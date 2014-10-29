from django.contrib import admin

from . import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    pass
