from django import forms
from .models import Grant


class UpdateClaim(forms.ModelForm):

    class Meta:
        model = Grant
        fields = ('assigned_data_centre',)

