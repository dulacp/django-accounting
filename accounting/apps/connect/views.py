from django.views import generic
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from accounting.apps.books.models import Organization


class RootRedirectionView(generic.TemplateView):
    """
    Redirect to the books if an organization is already configured

    Otherwise we begin the step by step creation process to help the user
    begin and configure his books
    """

    def get(self, *args, **kwargs):
        if Organization.objects.all().count():
            return HttpResponseRedirect(reverse('books:dashboard'))
