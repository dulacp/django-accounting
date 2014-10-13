from django.test import TestCase
from django.test.client import RequestFactory

from accounting.apps.context_processors import metadata


class TestLibsMetadata(TestCase):

    def setUp(self):
        factory = RequestFactory()
        self.request = factory.get('/')
        self.metadata = metadata(self.request)

    def test_has_version(self):
        self.assertTrue('version' in self.metadata)
        self.assertTrue('display_version' in self.metadata)
