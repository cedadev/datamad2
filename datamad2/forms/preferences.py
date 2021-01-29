# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Sep 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datamad2.search_indexes import GrantIndex
from datamad2.utils import removesuffix
from .search import DatamadFacetedSearchForm

facet_fields = [
        'assigned_datacentre',
        'labels',
        'other_datacentre',
        'secondary_classification',
        'grant_status',
        'grant_type',
        'scheme',
        'call',
        'facility',
        'lead',
        'ncas',
        'nceo',
        'dmp_agreed',
        'documents_attached',
        'visible'
    ]


class FacetPreferencesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

        igx = GrantIndex()
        # preference_fields = [removesuffix(field, '_exact') for field in igx.field_map if field.endswith('_exact')]
        # print(preference_fields)
        # for f in ['grant_ref', 'grant_holder', 'grant_title']:
        #     preference_fields.remove(f)

        preference_fields = facet_fields

        for field in preference_fields:
            self.fields[field] = forms.BooleanField(required=False)

class SortByPreferencesForm(forms.Form):

    sort_by = forms.ChoiceField(choices=DatamadFacetedSearchForm.CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False