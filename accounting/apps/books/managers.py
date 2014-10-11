from datetime import date

from django.db import models


class InvoiceQuerySet(models.QuerySet):
    def draft(self):
        return self.filter(draft=True)

    def dued(self):
        return self.filter(date_issued__lte=date.today(),
                           draft=False,
                           paid=False)
