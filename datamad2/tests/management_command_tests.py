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

from datamad2.models import ImportedGrant


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

    def test_import_from_file(self):
        """
        The test file contains a duplicate grant reference. This simulates
        running the command more than once. Checks that when running more than
        once and the data doesn't change, we are not creating another record.
        """
        
        csv_path = os.path.join(
                os.path.dirname(__file__),
                'files/siebel_csv/siebel_sample.csv'
        )
        
        self.call_command(file=csv_path)
        
        igs = ImportedGrant.objects.filter(grant_ref='NE/H014888/1')
        
        self.assertEqual(len(igs), 1)

