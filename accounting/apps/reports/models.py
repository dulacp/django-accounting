from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class BusinessSettings(models.Model):
    BUSINESS_TYPE_SOLE_PROPRIETORSHIP = 'sole_proprietorship'
    BUSINESS_TYPE_PARTNERSHIP = 'partnership'
    BUSINESS_TYPE_CORPORATION = 'corporation'
    BUSINESS_TYPE_CHOICES = (
        (BUSINESS_TYPE_SOLE_PROPRIETORSHIP, "Sole Proprietorship"),
        (BUSINESS_TYPE_PARTNERSHIP, "Partnership"),
        (BUSINESS_TYPE_CORPORATION, "Corporation"),
    )
    business_type = models.CharField(max_length=50,
                                     choices=BUSINESS_TYPE_CHOICES)

    # optionnaly linked to an organization
    # for automated behaviors during cross-organizations invoicing
    organization = models.OneToOneField('books.Organization',
                                        related_name="business_settings",
                                        blank=True, null=True)

    class Meta:
        pass


class FinancialSettings(models.Model):
    financial_year_end_day = models.PositiveSmallIntegerField(default=31,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(31)
        ])
    financial_year_end_month = models.PositiveSmallIntegerField(default=12,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(12)
        ])

    tax_id_number = models.CharField(max_length=150,
                                     blank=True, null=True)
    tax_id_display_name = models.CharField(max_length=150,
                                           blank=True, null=True)

    TAX_PERIOD_MONTHLY = 'monthly'      # 1 month
    TAX_PERIOD_BIMONTHLY = 'bimonthly'  # 2 months
    TAX_PERIOD_QUARTER = 'quarter'      # 3 months
    TAX_PERIOD_HALF = 'half'            # 6 months
    TAX_PERIOD_YEAR = 'year'            # 12 months
    TAX_PERIOD_CHOICES = (
        (TAX_PERIOD_MONTHLY, "1 month"),
        (TAX_PERIOD_BIMONTHLY, "2 months"),
        (TAX_PERIOD_QUARTER, "3 months"),
        (TAX_PERIOD_HALF, "6 months"),
        (TAX_PERIOD_YEAR, "1 year"),
    )
    tax_period = models.CharField("Tax Period",
                                  max_length=20,
                                  choices=TAX_PERIOD_CHOICES)

    # optionnaly linked to an organization
    # for automated behaviors during cross-organizations invoicing
    organization = models.OneToOneField('books.Organization',
                                        related_name="financial_settings",
                                        blank=True, null=True)

    class Meta:
        pass


class PayRunSettings(models.Model):
    salaries_follow_profits = models.BooleanField(default=False)

    PAYRUN_MONTHLY = 'monthly'      # 1 month
    # PAYRUN_QUARTER = 'quarter'      # 3 months
    PAYRUN_CHOICES = (
        (PAYRUN_MONTHLY, "monthly"),
    )
    payrun_period = models.CharField("Payrun Period",
                                     max_length=20,
                                     choices=PAYRUN_CHOICES,
                                     default=PAYRUN_MONTHLY)

    # optionnaly linked to an organization
    # for automated behaviors during cross-organizations invoicing
    organization = models.OneToOneField('books.Organization',
                                        related_name="payrun_settings",
                                        blank=True, null=True)

    class Meta:
        pass
