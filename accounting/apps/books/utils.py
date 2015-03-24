from django.db.models import Q


class OrganizationManager(object):
    selected_organization_key = 'selected_organization_pk'

    def get_user_organizations(self, user):
        # To avoid circular imports
        from .models import Organization

        orgas = (Organization.objects
            .filter(Q(members=user) | Q(owner=user))
            .distinct())
        return orgas

    def set_selected_organization(self, request, organization):
        key = self.selected_organization_key
        request.session[key] = organization.pk

    def get_selected_organization(self, request):
        key = self.selected_organization_key
        if key not in request.session:
            return

        # To avoid circular imports
        from .models import Organization

        pk = request.session[key]
        organization = Organization.objects.get(pk=pk)
        return organization


organization_manager = OrganizationManager()


class BaseNumberGenerator(object):
    """
    Simple object for generating sale numbers.
    """

    def next_number(self, organization):
        raise NotImplementedError


class EstimateNumberGenerator(BaseNumberGenerator):

    def next_number(self, organization):
        last = organization.estimates.all().order_by('-number').first()
        if last is not None:
            last_number = int(last.number)
        else:
            last_number = 0
        return last_number + 1


class InvoiceNumberGenerator(BaseNumberGenerator):

    def next_number(self, organization):
        last = organization.invoices.all().order_by('-number').first()
        if last is not None:
            last_number = int(last.number)
        else:
            last_number = 0
        return last_number + 1


class BillNumberGenerator(BaseNumberGenerator):

    def next_number(self, organization):
        last = organization.bills.all().order_by('-number').first()
        if last is not None:
            last_number = int(last.number)
        else:
            last_number = 0
        return last_number + 1


class ExpenseClaimNumberGenerator(BaseNumberGenerator):

    def next_number(self, organization):
        last = organization.expense_claims.all().order_by('-number').first()
        if last is not None:
            last_number = int(last.number)
        else:
            last_number = 0
        return last_number + 1
