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
from django.test import override_settings

# Datamad imports
from datamad2 import models

# Python imports
import os

ISSUE_TYPE_FIELD_MAPPING = {
    'start_date_field': 'customfield_13567', 'end_date_field': 'customfield_13568',
    'grant_ref_field': 'customfield_13569', 'pi_field': 'customfield_11453',
    'research_org_field': 'customfield_13573', 'primary_datacentre_field': 'customfield_11663',
    'amount_awarded_field': 'customfield_13578', 'grant_type_field': 'customfield_13585',
    'lead_grant_field': 'customfield_13586', 'parent_grant_field': 'customfield_13587',
    'child_grants_field': 'customfield_13588', 'email_field': 'customfield_13572',
    'other_datacentre_field': 'customfield_11664'}


@override_settings(MEDIA_ROOT=os.path.join(
    os.path.dirname(__file__),
    'files/'
))
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
            issuetype=10602,
            **ISSUE_TYPE_FIELD_MAPPING
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
            alt_data_contact='alt data contact',
            alt_data_contact_email='alt data contact email',
            alt_data_contact_phone='0800 000 0000',
            assigned_data_centre=cls.DATACENTRE,
            other_data_centre=None,
            hide_record=False,
            date_contacted_pi='2019-12-25',
            will_grant_produce_data=True,
            datasets_delivered=False,
            sanctions_recommended=False,
            case_for_support_found=True,
            claimed=True,
            updated_imported_grant=False,
            science_area='great science',
            jira_ticket='',
            dmp_agreed=False,

        )

        # Create the associated imported grant
        cls.IMPORTED_GRANT = models.ImportedGrant.objects.create(
            grant=cls.GRANT,
            grant_ref='NE/00001/1',
            title='Test grant for testing',
            abstract='Really long abstract',
            creation_date='2020-10-23 15:00',
            grant_status='Active',
            amount_awarded=100000,
            call='18GCRFHubsFull',
            overall_score=5,
            facility='ARCHER',
            grant_type='Science Delivery (RP)',
            scheme='IOF',
            lead_grant=True,
            parent_grant=None,
            grant_holder='A Professor of some sort',
            department='Environmental Science',
            research_org='A Uni',
            address1='address 1',
            address2='address 2',
            city='city',
            post_code='postcode',
            email='test@email.com',
            work_number='0800 0000 000',
            data_contact='A professor',
            data_contact_email='professor@email.com',
            data_contact_phone='0800 0000 000',
            routing_classification='Atmospheric',
            secondary_classification=None,
            science_area='Terrestrial: 10% Marine: 10% Atmospheric: 80%',
            ncas=True,
            nceo=False,
            comments='',
            proposed_start_date='2020-10-23',
            proposed_end_date='2020-10-23',
            actual_start_date='2020-10-23',
            actual_end_date='2020-10-23',
            objectives=''
        )

        cls.DATA_FORMAT = models.DataFormat.objects.create(
            datacentre=cls.DATACENTRE,
            format='netCDF'
        )

        cls.PRESERVATION_PLAN = models.PreservationPlan.objects.create(
            datacentre=cls.DATACENTRE,
            short_name='keep_forever',
            description="Don't delete this data"
        )

        cls.DOCUMENT_TEMPLATE = models.DocumentTemplate.objects.create(
            datacentre=cls.DATACENTRE,
            template=os.path.join(
                os.path.dirname(__file__),
                'files/templates/document_template_test.docx'
            ),
            name='Test Document',
            description='Test document to highlight all the different possibilities when'
                        ' generating a document from a template'
        )

        # Create data products
        ## Digital Data Product
        models.DataProduct.objects.create(
            data_product_type='digital',
            grant=cls.GRANT,
            description='Digital product description',
            contact='Professor Producer',
            data_volume=1000000000,
            data_format=cls.DATA_FORMAT,
            delivery_date='2020-12-25',
            embargo_date='2020-12-25',
            doi=True,
            preservation_plan=cls.PRESERVATION_PLAN,
            additional_comments='None'
        )

        ## Model Source Data Product
        models.DataProduct.objects.create(
            data_product_type='model_source',
            grant=cls.GRANT,
            name='Climate Model',
            contact='Professor Producer',
            description='Digital product description',
            sample_destination='GitHub',
            additional_comments='None'
        )

        ## Physical Data Product
        models.DataProduct.objects.create(
            data_product_type='physical',
            grant=cls.GRANT,
            name='Piece of rock',
            contact='Professor Producer',
            sample_type='Geological sample',
            sample_destination='the vault',
            additional_comments='None'

        )

        ## Hard-copy Data Product
        models.DataProduct.objects.create(
            data_product_type='hardcopy',
            grant=cls.GRANT,
            name='paper copy',
            contact='Professor Producer',
            data_format=models.DataFormat.objects.create(datacentre=cls.DATACENTRE,
                                          format='paper'),
            issues='None',
            delivery_date='2020-12-25',
            additional_comments='None'
        )

        ## Third-party Data Product
        models.DataProduct.objects.create(
            data_product_type='third_party',
            grant=cls.GRANT,
            name='weblink',
            contact='Professor Producer',
            data_location='github url',
            description='link to some data',
            data_volume=1000000000,
            responsibility='VIP',
            issues='None',
            additional_comments='None'
        )
