# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Sep 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django import forms
from datamad2.models import DataProduct, Grant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DataProductBaseFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))
        self.fields['grant_id'] = forms.IntegerField(required=False, widget=forms.HiddenInput)

    def save(self, **kwargs):
        # Save the related grant for this data product
        self.instance.grant = Grant.objects.get(pk=self.cleaned_data['grant_id'])
        return super().save()


class DataProductMetaBase:
    widgets = {
        'data_product_type': forms.HiddenInput
    }

    fields = ['data_product_type']


class DigitalDataProductForm(DataProductBaseFormMixin, forms.ModelForm):

    class Meta(DataProductMetaBase):
        model = DataProduct
        fields = [
            'description',
            'contact',
            'data_volume',
            'delivery_date',
            'embargo_date',
            'doi',
            'preservation_plan',
            'additional_comments',
        ] + DataProductMetaBase.fields


class ModelSourceDataProductForm(DataProductBaseFormMixin, forms.ModelForm):
    class Meta(DataProductMetaBase):
        model = DataProduct
        fields = [
            'name',
            'contact',
            'description',
            'sample_destination',
            'additional_comments'
        ] + DataProductMetaBase.fields


class PhysicalDataProductForm(DataProductBaseFormMixin, forms.ModelForm):
    class Meta(DataProductMetaBase):
        model = DataProduct
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments'
        ] + DataProductMetaBase.fields


class HardcopyDataProductForm(DataProductBaseFormMixin, forms.ModelForm):
    class Meta(DataProductMetaBase):
        model = DataProduct
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments'
        ] + DataProductMetaBase.fields


class ThirdPartyDataProductForm(DataProductBaseFormMixin, forms.ModelForm):
    class Meta(DataProductMetaBase):
        model = DataProduct
        fields = [
            'name',
            'contact',
            'data_location',
            'description',
            'data_volume',
            'responsibility',
            'issues',
            'additional_comments'
        ] + DataProductMetaBase.fields