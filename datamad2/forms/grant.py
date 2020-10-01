# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '25 Sep 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


from django import forms
from datamad2.models import Grant


class UpdateClaimForm(forms.ModelForm):

    class Meta:
        model = Grant
        fields = ('assigned_data_centre',)


class DateInput(forms.DateInput):
    input_type = 'date'


class GrantInfoForm(forms.ModelForm):

    class Meta:
        model = Grant
        fields = (
            'alt_data_contact',
            'alt_data_contact_email',
            'alt_data_contact_phone',
            'other_data_centre',
            'date_contacted_pi',
            'will_grant_produce_data',
            'datasets_delivered',
            'sanctions_recommended',
            'dmp_agreed'
        )
        widgets = {'date_contacted_pi': DateInput()}












