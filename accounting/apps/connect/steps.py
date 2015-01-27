from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from accounting.apps.books.models import Organization


class StepOptions(object):
    """
    Meta class options for a `BaseStep` subclass
    """
    def __init__(self, meta):
        self.name = getattr(meta, 'name', ())
        assert isinstance(self.name, (str)), '`name` must be a string instance'


class BaseStep(object):
    """
    Abstract class to subclass to create a getting started step
    """
    user = None

    _completion = None
    _options_class = StepOptions

    class StepOptions:
        name = "<Abstract>"

    def __init__(self, user):
        super().__init__()
        self.opts = self._options_class(getattr(self, 'StepOptions', None))
        self.user = user

    @property
    def completed(self):
        if self._completion is None:
            self._completion = self.check_completion()
        return self._completion

    def check_completion(self):
        """
        Implement the logic of the step
        and returns a boolean
        """
        raise NotImplementedError

    def get_action_url(self):
        """Returns the url to complete the step"""
        pass


class CreateOrganizationStep(BaseStep):
    """
    At least one organization has been created
    """

    class StepOptions:
        name = "Create an Organization"

    def check_completion(self):
        count = Organization.objects.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('books:organization-create')


class ConfigureTaxRatesStep(BaseStep):
    """
    At least one tax rate has been added (even if the rate is 0)
    """

    class StepOptions:
        name = "Configure Tax Rates"

    def check_completion(self):
        orga = Organization.objects.all().first()
        count = orga.tax_rates.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('books:tax_rate-create')


class ConfigureBusinessSettingsStep(BaseStep):
    """
    The associated business settings has been completed
    """

    class StepOptions:
        name = "Configure Business Settings"

    def check_completion(self):
        # TODO support multiple organizations checking with substeps
        orga = Organization.objects.all().first()
        settings = orga.business_settings
        try:
            settings.full_clean()
        except ValidationError:
            return False
        return True

    def get_action_url(self):
        return reverse('reports:settings-business')


class ConfigureFinancialSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Financial Settings"

    def check_completion(self):
        # TODO support multiple organizations checking with substeps
        orga = Organization.objects.all().first()
        settings = orga.financial_settings
        try:
            settings.full_clean()
        except ValidationError:
            return False
        return True

    def get_action_url(self):
        return reverse('reports:settings-financial')


class AddEmployeesStep(BaseStep):

    class StepOptions:
        name = "Add Employees"

    def check_completion(self):
        orga = Organization.objects.all().first()
        count = orga.employees.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('people:employee-create')


class ConfigurePayRunSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Pay Run Settings"

    def check_completion(self):
        # TODO support multiple organizations checking with substeps
        orga = Organization.objects.all().first()
        settings = orga.payrun_settings
        try:
            settings.full_clean()
        except ValidationError:
            return False
        return True

    def get_action_url(self):
        return reverse('reports:settings-payrun')


class AddFirstClientStep(BaseStep):

    class StepOptions:
        name = "Add the first Client"

    def check_completion(self):
        orga = Organization.objects.all().first()
        count = orga.clients.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('people:client-create')


class AddFirstInvoiceStep(BaseStep):

    class StepOptions:
        name = "Add the first Invoice"

    def check_completion(self):
        orga = Organization.objects.all().first()
        count = orga.invoices.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('books:invoice-create')
