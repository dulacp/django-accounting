# encoding: utf-8

import datetime

from django.test import TransactionTestCase, TestCase
from django.test.utils import override_settings
from django.core.urlresolvers import ResolverMatch

from accounting.libs.utils import queryset_iterator

from tests._site.model_tests_app.models import MockModelWitNoFields

import mock


class TestQuerysetIteratorHelper(TransactionTestCase):

    def setUp(self):
        self.model = MockModelWitNoFields
        # generate a bunch of objects
        for index in range(21):
            self.model.objects.create()

    ######################################################################
    # The two following tests are skipped because it fails for an
    # unknown reason
    #
    # EDIT: the displayed error is variable and changed times to times
    #
    # TODO fix those 2 tests
    #
    # CommandError: Database test_ledej_development couldn't be flushed.
    # Possible reasons:
    #   * The database isn't running or isn't configured correctly.
    #   * At least one of the expected database tables doesn't exist.
    #   * The SQL was invalid.
    # Hint: Look at the output of 'django-admin.py sqlflush'. That's the
    # SQL this command wasn't able to run.
    ######################################################################

    # def test_get_every_objects_with_small_chunksize(self):
    #     counter = 0
    #     for obj in queryset_iterator(self.model.objects.all(),
    #                                  chunksize=10):
    #         counter += 1
    #     self.assertEqual(counter, 21)

    # def test_cut_the_queryset_into_chunks(self):
    #     def chunkify():
    #         for obj in queryset_iterator(self.model.objects.all(),
    #                                      chunksize=10):
    #             pass
    # an extra call is made to check that there is no more rows
    # so it cuts into 3 chunks + 1 last call
    #     self.assertNumQueries(4, chunkify)
