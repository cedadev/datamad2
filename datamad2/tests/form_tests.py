# encoding: utf-8
"""
Tests for forms and form validation within datamad
"""
__author__ = 'Richard Smith'
__date__ = '23 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .base import DatamadTestCase
from datamad2.forms import *


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