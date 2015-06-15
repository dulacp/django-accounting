from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from . import models


@admin.register(models.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TaxRate)
class TaxRateAdmin(admin.ModelAdmin):
    pass


class PaymentInline(GenericTabularInline):
    model = models.Payment
    extra = 1


class EstimateLineInline(admin.TabularInline):
    model = models.EstimateLine
    extra = 1


@admin.register(models.Estimate)
class EstimateAdmin(admin.ModelAdmin):
    inlines = (
        EstimateLineInline,
    )
    readonly = (
        'total_incl_tax', 'total_excl_tax',
    )


class InvoiceLineInline(admin.TabularInline):
    model = models.InvoiceLine
    extra = 1


@admin.register(models.Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    inlines = (
        InvoiceLineInline,
        PaymentInline,
    )
    readonly = (
        'total_incl_tax', 'total_excl_tax',
    )


class BillLineInline(admin.TabularInline):
    model = models.BillLine
    extra = 1


@admin.register(models.Bill)
class BillAdmin(admin.ModelAdmin):
    inlines = (
        BillLineInline,
        PaymentInline,
    )
    readonly = (
        'total_incl_tax', 'total_excl_tax',
    )


class ExpenseClaimLineInline(admin.TabularInline):
    model = models.ExpenseClaimLine
    extra = 1


@admin.register(models.ExpenseClaim)
class ExpenseClaimAdmin(admin.ModelAdmin):
    inlines = (
        ExpenseClaimLineInline,
        PaymentInline,
    )
    readonly = (
        'total_incl_tax', 'total_excl_tax',
    )


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass
