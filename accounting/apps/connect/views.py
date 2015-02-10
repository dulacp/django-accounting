from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from accounting.apps.books.models import Organization
from .steps import (
    CreateOrganizationStep,
    ConfigureTaxRatesStep,
    ConfigureBusinessSettingsStep,
    ConfigureFinancialSettingsStep,
    AddEmployeesStep,
    ConfigurePayRunSettingsStep,
    AddFirstClientStep,
    AddFirstInvoiceStep)


class RootRedirectionView(generic.View):
    """
    Redirect to the books if an organization is already configured

    Otherwise we begin the step by step creation process to help the user
    begin and configure his books
    """

    def get(self, *args, **kwargs):
        if Organization.objects.all().count():
            return HttpResponseRedirect(reverse('books:dashboard'))


class GettingStartedView(generic.TemplateView):
    template_name = "connect/getting_started.html"

    def get_steps(self, request):
        user = request.user
        steps = steps = [
            CreateOrganizationStep(user),
            ConfigureTaxRatesStep(user),
            ConfigureBusinessSettingsStep(user),
            ConfigureFinancialSettingsStep(user),
            AddEmployeesStep(user),
            ConfigurePayRunSettingsStep(user),
            AddFirstClientStep(user),
            AddFirstInvoiceStep(user),
        ]
        return steps

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        request = self.request
        steps = self.get_steps(self.request)
        uncomplete_filter = lambda s: not s.completed(request)
        uncompleted_steps = list(filter(uncomplete_filter, steps))
        try:
            next_step = next(s for s in uncompleted_steps)
        except StopIteration:
            next_step = None

        ctx['steps'] = steps
        ctx['next_step'] = next_step
        ctx['all_steps_completed'] = bool(next_step is None)

        return ctx

    def post(self, request, *args, **kwargs):
        steps = self.get_steps(request)
        uncompleted_steps = filter(lambda s: not s.completed(request), steps)
        if not len(uncompleted_steps):
            return super().post(request, *args, **kwargs)

        # unmark the session as getting started
        request.sessions['getting_started_done'] = True
        return HttpResponseRedirect(reverse('books:dashboard'))
