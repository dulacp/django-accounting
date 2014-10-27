from django.contrib import admin

from . import models


@admin.register(models.FinancialSettings)
class FinancialSettingsAdmin(admin.ModelAdmin):
    pass
