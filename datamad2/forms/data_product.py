# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Sep 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django import forms
from django.forms import formset_factory
from django.forms import inlineformset_factory
from datamad2.models import DataProduct, Grant
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class DigitalDataProductForm(forms.ModelForm):

    grant_id = forms.IntegerField(required=False, widget=forms.HiddenInput)

    class Meta:
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
            'data_product_type',
        ]

        widgets = {
            'data_product_type': forms.HiddenInput
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))

    def save(self, **kwargs):
        # Save the related grant for this data product
        self.instance.grant = Grant.objects.get(pk=self.cleaned_data['grant_id'])
        return super().save()


class ModelSourceDataProductForm(forms.ModelForm):
    class Meta:
        model = DataProduct
        fields = [
            'name',
            'contact',
            'description',
            'sample_destination',
            'additional_comments'
        ]


class PhysicalDataProductForm(forms.ModelForm):
    class Meta:
        model = DataProduct
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments'
        ]


class HardcopyDataProductForm(forms.ModelForm):
    class Meta:
        model = DataProduct
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments'
        ]


class ThirdPartyDataProductForm(forms.ModelForm):
    class Meta:
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
        ]


# class DataProductFormsetHelper(FormHelper):
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.form_tag = False
#

# DigitalDataProductFormset = inlineformset_factory(Grant, DataProduct, form=DigitalDataProductForm, extra=1, can_delete=True)

# ModelSourceDataProductFormset = inlineformset_factory(Grant, DataProduct,  extra=0)

# ModelSourceDataProductFormset = formset_factory(ModelSourceDataProductForm, extra=0, can_delete=True)
# PysicalDataProductFormset = formset_factory(PysicalDataProductForm, extra=0, can_delete=True)
# HardcopyDataProductFormset = formset_factory(HardcopyDataProductForm, extra=0, can_delete=True)
# ThirdPartyDataProductFormset = formset_factory(ThirdPartyDataProductForm, extra=0, can_delete=True)
