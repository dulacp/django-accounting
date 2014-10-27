from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class FinancialSettings(models.Model):
    financial_year_end_day = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(31)
    ])
    financial_year_end_month = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(12)
    ])

    tax_id_number = models.CharField(max_length=150,
                                     blank=True, null=True)
    tax_id_display_name = models.CharField(max_length=150,
                                           blank=True, null=True)

    TAX_PERIOD_MONTHLY =   'monthly'      # 1 month
    TAX_PERIOD_BIMONTHLY = 'bimonthly'    # 2 months
    TAX_PERIOD_QUARTER =   'quarter'      # 3 months
    TAX_PERIOD_HALF =      'half'         # 6 months
    TAX_PERIOD_YEAR =      'year'         # 12 months
    TAX_PERIOD_CHOICES = (
        (TAX_PERIOD_MONTHLY,   "1 month"),
        (TAX_PERIOD_BIMONTHLY, "2 months"),
        (TAX_PERIOD_QUARTER,   "3 months"),
        (TAX_PERIOD_HALF,      "6 months"),
        (TAX_PERIOD_YEAR,      "1 year"),
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

    def __str__(self):
        return self.name

    def active_address_fields(self):
        """
        Return the non-empty components of the address
        """
        fields = [self.address_line_1, self.address_line_2,
                  self.city, self.postal_code, self.country]
        fields = [f.strip() for f in fields if f]
        return fields

    def full_address(self, separator="\n"):
        return separator.join(filter(bool, self.active_address_fields()))
