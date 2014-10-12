from django.contrib import admin

from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


class InvoiceLineInline(admin.TabularInline):
    model = models.InvoiceLine
    extra = 1


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (
        InvoiceLineInline,
    )


class BillLineInline(admin.TabularInline):
    model = models.BillLine
    extra = 1


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = (
        BillLineInline,
    )
