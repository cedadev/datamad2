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
from datamad2.search_indexes import ImportedGrantIndex
from datamad2.utils import removesuffix


class FacetPreferencesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Update Preferences'))

        igx = ImportedGrantIndex()
        preference_fields = [removesuffix(field, '_exact') for field in igx.field_map if field.endswith('_exact')]

        for field in preference_fields:
            self.fields[field] = forms.BooleanField(required=False)