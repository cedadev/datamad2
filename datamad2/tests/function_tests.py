# encoding: utf-8
"""
Tests for functions within datamad
"""
__author__ = 'Richard Smith'
__date__ = '23 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .base import DatamadTestCase


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
