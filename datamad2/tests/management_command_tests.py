# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '20 Nov 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.test import TestCase
from django.core.management import call_command

from io import StringIO
import os

from datamad2.models import ImportedGrant, Grant


class ManagementTestCase(TestCase):

    MANAGEMENT_COMMAND = None

    def call_command(self, *args, **kwargs):
        call_command(
            self.MANAGEMENT_COMMAND,
            *args,
            stdout=StringIO(),
            stderr=StringIO(),
            **kwargs,
        )


class ImportDatabaseManagementTests(ManagementTestCase):

    MANAGEMENT_COMMAND = 'import_database'
    CSV_PATH = os.path.join(
                os.path.dirname(__file__),
                'files/siebel_csv/siebel_sample.csv'
        )

    def test_import_from_file(self):
        """
        The test file contains a duplicate grant reference. This simulates
        running the command more than once. Checks that when running more than
        once and the data doesn't change, we are not creating another record.
        """
        
        self.call_command(file=self.CSV_PATH)
        
        igs = ImportedGrant.objects.filter(grant_ref='NE/H014888/1')
        
        self.assertEqual(len(igs), 1)

    def test_creation_date_on_import(self):
        """
        Test that the creation dates for the various components works as expected.
        New Grant:
            - Grant created and creation_date set
            - ImportedGrant created and creation_date set
            - updated_date property matches new imported grant creation_date

        ImportedGrant Updated:
            - Grant creation_date stays the same
            - New ImportedGrant created and creation_date set
            - updated_date property matches new imported grant creation_date
        """

        self.call_command(file=self.CSV_PATH)

        new_grant = Grant.objects.get(grant_ref='NE/H014330/1')

        # Test where there are no changes to ImportedGrant
        self.assertTrue(new_grant.date_added)
        self.assertTrue(new_grant.importedgrant.creation_date)
        self.assertEqual(new_grant.importedgrant.creation_date, new_grant.updated_date)

        # Re-run command where there is a minor change
        csv_path = os.path.join(
            os.path.dirname(__file__),
            'files/siebel_csv/siebel_sample_modified.csv'
        )

        self.call_command(file=csv_path)

        # Test where there are updates to the imported grant and so the dates should change
        rerun_grant = Grant.objects.get(grant_ref='NE/H014330/1')

        self.assertEqual(new_grant.date_added, rerun_grant.date_added)
        self.assertEqual(ImportedGrant.objects.filter(grant_ref='NE/H014330/1').count(), 2)
        self.assertEqual(rerun_grant.importedgrant.creation_date, new_grant.updated_date)


