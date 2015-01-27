from decimal import Decimal as D

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    name = models.CharField(max_length=150)

    # address
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128,
                                      blank=True, null=True)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=7)
    country = models.CharField(max_length=50)

    organization = models.ForeignKey('books.Organization',
                                     related_name="clients")

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


class Employee(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(max_length=254)

    payroll_tax_rate = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        validators=[
            MinValueValidator(D('0')),
            MaxValueValidator(D('1'))
        ]
    )

    salary_follows_profits = models.BooleanField(default=False)
    shares_percentage = models.DecimalField(
        max_digits=6,
        decimal_places=5,
        validators=[
            MinValueValidator(D('0')),
            MaxValueValidator(D('1'))
        ]
    )

    organization = models.ForeignKey('books.Organization',
                                     related_name="employees")

    class Meta:
        pass

    def __str__(self):
        return "{}".format(self.composite_name)

    @property
    def composite_name(self):
        return "{} {}".format(self.first_name, self.last_name)
