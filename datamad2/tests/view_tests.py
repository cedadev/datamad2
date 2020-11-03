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
from django.urls import reverse

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

    VIEW_URL = '/'

    def test_preferred_sorting(self):
        """
        Check that the logged in user gets redirected to their
        :return:
        """

        self.client.force_login(self.USER)
        response = self.client.get(self.VIEW_URL)
        self.assertEqual(f'{reverse("grant_list")}?sort_by={self.USER.preferred_sorting}', response.url)


    def test_csrf_cookie(self):
        """
        Check that the CSRF token is embedded in the main grant page to allow the AJAX
        claim_grant process to work https://github.com/cedadev/datamad2/issues/300
        """
                        
        self.client.force_login(self.USER)
        response = self.client.get(f'{self.VIEW_URL}?sort_by={self.USER.preferred_sorting}')
        self.assertIn('csrfmiddlewaretoken', str(response.content))

    def test_filters_with_preferred_sorting(self):
        """
        Check that if the user has a preferred sorting, the other filters are correctly applied.
        :return:
        """

        self.client.force_login(self.USER)

        response = self.client.get(f'{self.VIEW_URL}?selected_facets=assigned_datacentre:Unassigned')

        self.assertEqual(f'/?selected_facets=assigned_datacentre%3AUnassigned&sort_by={self.USER.preferred_sorting}', response.url)

