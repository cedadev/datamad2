# Django imports
from django.test import TestCase, Client
from django.urls import reverse

# Datamad imports
from datamad2 import models
from datamad2.forms import *


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


class TestDataProductForm(DatamadTestCase):
    """
    Tests relating to the Data Product forms
    """

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.TEST_DATA = {
            'grant': cls.GRANT,
            'grant_id': cls.GRANT.pk,
            'data_product_type': '',
            'name': 'test',
            'contact': 'test_contact',
            'data_format': cls.DATA_FORMAT.pk,
            'preservation_plan': cls.PRESERVATION_PLAN.pk,
            'description': 'This is a test data product',
            'data_volume': '10GB',
            'delivery_date': '22/10/2020',
            'embargo_date': '25/12/2020',
            'doi': True,
            'sample_type': 'sample',
            'sample_destination': 'sample sample',
            'issues': 'none',
            'data_location': 'here',
            'responsibility': 'a person',
            'additional_comments': 'There are none'
        }

    def populate_form(self, form, data_product_type, extra_data=None):
        """
        Abstraction for form population to reduce repetition.
        :param form: Form to test
        :param data_product_type: Relevant data product
        :param extra_data: Dict to merge into main data to override defaults
        """

        fields = form.base_fields.keys()

        data = {k:v for k,v in self.TEST_DATA.items() if k in fields}
        data['data_product_type'] = data_product_type

        if extra_data:
            data.update(extra_data)

        return form(data=data)

    def test_digital_dataproduct(self):
        data_product_type = 'digital'
        form = DigitalDataProductForm

        instance = self.populate_form(form, data_product_type)
        self.assertTrue(instance.is_valid())

    def test_model_dataproduct(self):
        data_product_type = 'model_source'
        form = ModelSourceDataProductForm

        instance = self.populate_form(form, data_product_type)
        self.assertTrue(instance.is_valid())

    def test_physical_dataproduct(self):
        data_product_type = 'physical'
        form = PhysicalDataProductForm

        instance = self.populate_form(form, data_product_type)
        self.assertTrue(instance.is_valid())

    def test_hardcopy_dataproduct(self):
        form = HardcopyDataProductForm
        data_product_type = 'hardcopy'

        instance = self.populate_form(form, data_product_type)
        self.assertTrue(instance.is_valid())

    def test_thirdparty_dataproduct(self):

        form = ThirdPartyDataProductForm
        data_product_type = 'digital'

        instance = self.populate_form(form, data_product_type)
        self.assertTrue(instance.is_valid())

    def test_incorrect_date_format_validation(self):
        """
        If given date in incorrect format, date validation should fail
        """

        form = DigitalDataProductForm
        data_product_type = 'digital'
        extra_data = {
            'delivery_date': '10/21/2020'
        }

        instance = self.populate_form(form, data_product_type, extra_data)
        self.assertFalse(instance.is_valid())