# encoding: utf-8
"""
Base Test class which handles setting up the test database
"""
__author__ = 'Richard Smith'
__date__ = '23 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Django imports
from django.test import TestCase, Client

# Datamad imports
from datamad2 import models


class DatamadTestCase(TestCase):
    """
    Base class to build database instances for testing
    """

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        super().setUpClass()

    @classmethod
    def setUpTestData(cls):
        # Create the datacentre
        cls.DATACENTRE = models.DataCentre.objects.create(
            name='CEDA',
            jira_project='CEDA'
        )

        cls.ISSUETYPE = models.JIRAIssueType.objects.create(
            datacentre=cls.DATACENTRE,
            issuetype=10602
        )

        # Create a test user and associate datacentre
        cls.USER = models.User.objects.create(
            first_name='Test',
            last_name='User',
            email='test.user@testing.com',
            data_centre=cls.DATACENTRE,
            password='testingpassword',
            preferred_sorting='date_added'
        )

        # Create a grant
        cls.GRANT = models.Grant.objects.create(
            grant_ref='NE/00001/1',

        )

        # Create the associated imported grant
        cls.IMPORTED_GRANT = models.ImportedGrant.objects.create(
            grant=cls.GRANT,
            grant_ref='NE/00001/1',
            title='Test grant for testing',
            abstract='Really long abstract'
        )

        cls.DATA_FORMAT = models.DataFormat(
            datacentre=cls.DATACENTRE,
            format='netCDF'
        )

        cls.PRESERVATION_PLAN = models.PreservationPlan(
            datacentre=cls.DATACENTRE,
            short_name='keep_forever',
            description="Don't delete this data"
        )