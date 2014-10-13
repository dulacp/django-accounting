import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from django_dynamic_fixture import G

from accounting.apps.books.models import Organization


class TestUserBelongsToOrganization(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = G(User)

    def tearDown(self):
        self.user.delete()

    def test_no_organization_by_default(self):
        self.assertEquals(self.user.organizations.all().count(), 0)

    def test_belongs_to_an_organization(self):
        orga = G(Organization)
        orga.members.add(self.user)
        self.assertEquals(self.user.organizations.all().count(), 1)
