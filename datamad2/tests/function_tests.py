# encoding: utf-8
"""
Tests for functions within datamad
"""
__author__ = 'Richard Smith'
__date__ = '23 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Test imports
from .base import DatamadTestCase

# Django imports
from django.conf import settings

# Datamad imports
from datamad2.utils import generate_document_from_template
from datamad2.create_issue import map_datamad_to_jira

# Python imports
import shutil


def remove_generated_documents():
    shutil.rmtree(f'{settings.MEDIA_ROOT}/generated_documents')


class TestJIRAPush(DatamadTestCase):
    """
    Test the functionality surrounding JIRA ticket creation
    """

    def test_required_fields(self):
        """
        Tests whether the required fields can be accessed for the JIRA ticket
        :return:
        """

        issue_dict = {
            'project': str(self.USER.data_centre.jira_project),
            'summary': f'{self.IMPORTED_GRANT.grant_ref}:{self.IMPORTED_GRANT.title}',
            'description': self.IMPORTED_GRANT.abstract,
            'issuetype': {'id': str(self.USER.data_centre.jiraissuetype_set.first().issuetype)},
        }

        self.assertDictEqual(issue_dict, {
            'project': 'CEDA',
            'summary': 'NE/00001/1:Test grant for testing',
            'description': 'Really long abstract',
            'issuetype': {'id': str(self.USER.data_centre.jiraissuetype.issuetype)},
        })

    def test_jira_issue_field_mapping_evaluation(self):
        self.client.force_login(self.USER)
        request = self.client.request().wsgi_request

        issue_dict = map_datamad_to_jira(request, self.IMPORTED_GRANT)
        self.assertDictEqual(
            {'customfield_13567': '2020-10-23', 'customfield_13568': '2020-10-23', 'customfield_13569': 'NE/00001/1',
             'customfield_11453': 'A Professor of some sort', 'customfield_13573': 'A Uni',
             'customfield_11663': {'value': 'CEDA'}, 'customfield_13578': '100000',
             'customfield_13585': 'Science Delivery (RP)', 'customfield_13586': 'True', 'customfield_13588': '',
             'customfield_13572': 'test@email.com'}
            , issue_dict)


class TestDocumentGeneration(DatamadTestCase):

    def test_data_product_access(self):
        data_product_types = [
            'digital',
            'model_source',
            'physical',
            'hardcopy',
            'third_party'
        ]

        for product in data_product_types:
            data_products = getattr(self.GRANT, f'{product}_data_products')
            self.assertEqual(1, data_products.count())

    def test_generate_document(self):
        # Add task to remove generated documents
        self.addCleanup(remove_generated_documents)

        template = self.DOCUMENT_TEMPLATE
        context = {
            'grant': self.GRANT,
            'table_test': {
                'col_labels': ['col1', 'col2'],
                'table_contents': [
                    {'col1': 'row1col1', 'col2': 'row1col2'},
                    {'col1': 'row2col1', 'col2': 'row2col2'}
                ]
            }
        }

        doc = generate_document_from_template(template, context)
