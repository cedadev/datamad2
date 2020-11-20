# encoding: utf-8
"""
Tests on views within datamad
"""
__author__ = 'Richard Smith'
__date__ = '23 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Django imports
from django.urls import reverse, reverse_lazy
from django.test import RequestFactory

# Datamad Imports
from datamad2.views import DataFormatUpdateCreateView

# Test imports
from .base import DatamadTestCase

# Python imports
import unittest


class DatamadViewTestCase(DatamadTestCase):
    """
    Adds a view URL attribute to the test class
    for datamad view tests
    """
    
    VIEW_URL = None


class AnonymousUserGetViewTestMixin(DatamadViewTestCase):
    """
    Mixin to check that anonymous users are not able
    to view the selected views.

    Should be used with a DatamadViewTestCase
    """

    def test_anonymous_user(self):
        # Because this mixin inherits from DatamadViewTestCase, it gets
        # run as a test. This skips when it is not appropriate
        if type(self) is AnonymousUserGetViewTestMixin:
            self.skipTest("Dont run test on mixin")

        response = self.client.get(self.VIEW_URL)

        self.assertEqual(reverse('login'), response.url.split('?')[0])


class AnonymousUserPostViewTestMixin(DatamadViewTestCase):

    def test_anonymous_user(self):
        pass


class TestFacetedSearchPage(AnonymousUserGetViewTestMixin, DatamadViewTestCase):
    """
    Tests relating to the faceted search home page
    """

    VIEW_URL = reverse_lazy('grant_list')

    def test_preferred_sorting(self):
        """
        Check that the logged in user gets redirected to their
        :return:
        """

        self.client.force_login(self.USER)
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(f'{reverse("grant_list")}?sort_by={self.USER.preferred_sorting}', response.url)

    def test_filters_with_preferred_sorting(self):
        """
        Check that if the user has a preferred sorting, the other filters are correctly applied.
        :return:
        """

        self.client.force_login(self.USER)

        response = self.client.get(f'{self.VIEW_URL}?selected_facets=assigned_datacentre:Unassigned')

        self.assertEqual(f'/?selected_facets=assigned_datacentre%3AUnassigned&sort_by={self.USER.preferred_sorting}', response.url)


class TestUserEditPermissions(AnonymousUserGetViewTestMixin, DatamadViewTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.VIEW_URL = reverse('user_update', kwargs={
            'pk': cls.ADMINUSER.pk
        })

    def test_non_admin_user_edit(self):
        """
        A non-admin user should not be able to request to edit
        another users information
        """

        # Login as non admin user
        self.client.force_login(self.USER)

        response = self.client.get(self.VIEW_URL)
        self.assertEqual(403, response.status_code)

    def test_non_admin_edit_self(self):
        """
        A non admin user should be able to edit themselves
        """

        # Login as non admin user
        self.client.force_login(self.USER)

        # Change the view URL to match the logged in user
        self.VIEW_URL = reverse('user_update', kwargs={
            'pk': self.USER.pk
        })

        response = self.client.get(self.VIEW_URL)
        self.assertEqual(200, response.status_code)

    def test_admin_user(self):
        """
        An admin user should be able to edit another user
        """

        # Login as admin user
        self.client.force_login(self.ADMINUSER)

        # Change the view URL to match another user
        self.VIEW_URL = reverse('user_update', kwargs={
            'pk': self.USER.pk
        })

        response = self.client.get(self.VIEW_URL)
        self.assertEqual(200, response.status_code)


class TestUserList(DatamadViewTestCase):

    VIEW_URL = reverse_lazy('user_list')

    def test_non_admin_user_permissions(self):

        # Login as non-admin user
        self.client.force_login(self.USER)

        response = self.client.get(self.VIEW_URL)
        self.assertEqual(200, response.status_code)


class TestUpdateOrCreateMixin(DatamadViewTestCase):
    VIEW_URL = reverse_lazy('data_format_create')

    def test_create_new_data_format(self):
        """
        Check that when trying the create URL no object is
        returned
        """

        self.VIEW_URL = reverse_lazy('data_format_create')

        # Setup the request
        factory = RequestFactory()
        request = factory.get(self.VIEW_URL)

        # Get the view and try the method
        view = DataFormatUpdateCreateView()
        view.setup(request)
        object = view.get_object()

        self.assertIsNone(object)

    def test_update_existing_data_format(self):
        """
        Check that when trying the update URL only one
        object is returned
        """

        self.VIEW_URL = reverse_lazy('data_format_update', kwargs={'pk':1})

        # Setup the request
        factory = RequestFactory()
        request = factory.get(self.VIEW_URL)
        request.user = self.ADMINUSER

        # Get the view and try the method
        view = DataFormatUpdateCreateView()
        view.setup(request, pk=1)
        object = view.get_object()

        self.assertEqual(object.pk, self.DATA_FORMAT.pk)




