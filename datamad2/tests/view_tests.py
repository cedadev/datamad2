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


class TestFacetedSearchPage(DatamadTestCase):
    """
    Tests relating to the faceted search home page
    """

    def test_preferred_sorting(self):
        """
        Check that the logged in user gets redirected to their
        :return:
        """

        self.client.force_login(self.USER)
        response = self.client.get('/')
        self.assertEqual(f'{reverse("grant_list")}?sort_by={self.USER.preferred_sorting}', response.url)