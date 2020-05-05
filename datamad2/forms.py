from django import forms
from .models.grants import Grant


class UpdateClaim(forms.ModelForm):

    class Meta:
        model = Grant
        fields = ('assigned_data_centre',)


class DateInput(forms.DateInput):
    input_type = 'date'


class GrantInfoForm(forms.ModelForm):

    class Meta:
        model = Grant
        fields = ('alt_data_contact', 'alt_data_contact_email', 'alt_data_contact_phone', 'other_data_centre', 'date_contacted_pi',
                  'will_grant_produce_data', 'datasets_delivered', 'sanctions_recommended', 'case_for_support_found')
        widgets = {'date_contacted_pi': DateInput()}
