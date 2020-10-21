from django.test import TestCase, Client
from datamad2 import models


class DatamadTestCast(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = Client()
        super().setUpClass()


class TestJIRAPush(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Create the datacentre
        cls.dc = models.DataCentre.objects.create(
            name='CEDA',
            jira_project='CEDA'
        )

        cls.issuetype = models.JIRAIssueType.objects.create(
            datacentre=cls.dc,
            issuetype=10602
        )

        # Create a test user and associate datacentre
        cls.user = models.User.objects.create(
            first_name='Test',
            last_name='User',
            email='test.user@testing.com',
            data_centre = cls.dc,
            password='testingpassword'
        )

        # Create a grant
        cls.grant = models.Grant.objects.create(
            grant_ref='NE/00001/1'
        )

        # Create the associated imported grant
        cls.imported_grant = models.ImportedGrant.objects.create(
            grant=cls.grant,
            grant_ref='NE/00001/1',
            title='Test grant for testing',
            abstract='Really long abstract'
        )

    def test_required_fields(self):
        """
        Tests whether the required fields can be accessed for the JIRA ticket
        :return:
        """

        issue_dict = {
            'project': str(self.user.data_centre.jira_project),
            'summary': f'{self.imported_grant.grant_ref}:{self.imported_grant.title}',
            'description': self.imported_grant.abstract,
            'issuetype': {'id': str(self.user.data_centre.jiraissuetype_set.first().issuetype)},
        }

        self.assertDictEqual(issue_dict,{
            'project': 'CEDA',
            'summary': 'NE/00001/1:Test grant for testing',
            'description': 'Really long abstract',
            'issuetype': {'id': str(self.user.data_centre.jiraissuetype_set.first().issuetype)},
        })



