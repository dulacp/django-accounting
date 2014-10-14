from django.db import models


class Client(models.Model):
    name = models.CharField(max_length=150)

    # address
    address_line_1 = models.CharField(max_length=128)
    address_line_2 = models.CharField(max_length=128,
                                      blank=True, null=True)
    city = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=7)
    country = models.CharField(max_length=50)

    # optionnaly linked to an organization
    # for automated behaviors during cross-organizations invoicing
    organization = models.ForeignKey('books.Organization',
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
