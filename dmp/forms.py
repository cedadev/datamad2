from django import forms
from .models import DataProduct


class DataProductForm(forms.ModelForm):
    class Meta:
        model = DataProduct
        fields = '__all__'
