from django.core.urlresolvers import reverse


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

    class StepOptions:
        name = "Create an Organization"

    def check_completion(self):
        return False

    def get_action_url(self):
        return reverse('books:organization-create')


class ConfigureTaxRatesStep(BaseStep):

    class StepOptions:
        name = "Configure Tax Rates"

    def check_completion(self):
        return False

    def get_action_url(self):
        return reverse('books:tax_rate-create')


class ConfigureBusinessSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Business Settings"

    def check_completion(self):
        return False

    def get_action_url(self):
        return reverse('reports:settings-business')


class ConfigureFinancialSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Financial Settings"

    def check_completion(self):
        return False


class AddEmployeesStep(BaseStep):

    class StepOptions:
        name = "Add Employees"

    def check_completion(self):
        return False


class ConfigurePayRunSettingsStep(BaseStep):

    class StepOptions:
        name = "Configure Pay Run Settings"

    def check_completion(self):
        return False
