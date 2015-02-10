import logging

from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

from accounting.apps.books.utils import organization_manager
from accounting.apps.reports.models import BusinessSettings

logger = logging.getLogger(__name__)


class StepOptions(object):
    """
    Meta class options for a `BaseStep` subclass
    """
    def __init__(self, meta):
        self.name = getattr(meta, 'name', None)
        assert(isinstance(self.name, (str)),
            '`name` must be a string instance')
        self.description = getattr(meta, 'description', "")
        assert(isinstance(self.description, (str)),
            '`description` must be a string instance')


class BaseStep(object):
    """
    Abstract class to subclass to create a getting started step
    """
    user = None

    _completion = None
    _options_class = StepOptions

    class StepOptions:
        name = "<Abstract>"
        description = None

    def __init__(self, user):
        super().__init__()
        self.opts = self._options_class(getattr(self, 'StepOptions', None))
        self.user = user

    def completed(self, request):
        if self._completion is None:
            self._completion = self.check_completion(request)
        return self._completion

    def is_completed(self):
        """pre computed value, to be called in templates"""
        if self._completion is None:
            logger.error("`completed` needs to be run before using "
                         "this method")
            return False
        return self._completion

    def check_completion(self, request):
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
        description = "the organization is the foundation of the accounting " \
                      "system, tell Accountant-x more about it"

    def check_completion(self, request):
        orgas = organization_manager.get_user_organizations(request.user)
        count = orgas.count()
        return count > 0

    def get_action_url(self):
        return reverse('books:organization-create')


class ConfigureTaxRatesStep(BaseStep):
    """
    At least one tax rate has been added (even if the rate is 0)
    """

    class StepOptions:
        name = "Configure Tax Rates"
        description = "even if you are not subject to tax collecting rules " \
                      "you should create a 0% tax entry"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
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
        description = "for now there is not much thing, but please create it"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
        try:
            settings = orga.business_settings
            settings.full_clean()
        except BusinessSettings.DoesNotExist:
            return False
        except ValidationError:
            return False
        return True

    def get_action_url(self):
        return reverse('reports:settings-business')


class ConfigureFinancialSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Financial Settings"
        description = "tell Accountant-x what is your financial rulling rule"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
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
        description = "add at least one *employee*, even if you are giving " \
                      "yourself a salary that follows the profits"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
        count = orga.employees.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('people:employee-create')


class ConfigurePayRunSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Pay Run Settings"
        description = "tell to Accountant-x how you distribute salaries"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
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
        description = "close to the first invoice"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
        count = orga.clients.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('people:client-create')


class AddFirstInvoiceStep(BaseStep):

    class StepOptions:
        name = "Add the first Invoice"
        description = "finally create it !"

    def check_completion(self, request):
        orga = organization_manager.get_selected_organization(request)
        if orga is None:
            return False
        count = orga.invoices.all().count()
        return count > 0

    def get_action_url(self):
        return reverse('books:invoice-create')
