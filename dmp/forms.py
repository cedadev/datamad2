from django import forms
from .models import DataProduct, Project

class DateInput(forms.DateInput):
    input_type = 'date'

class DataProductForm(forms.ModelForm):
    class Meta:
        model = DataProduct
        fields = '__all__'
        widgets = {'deliverydate': DateInput()}


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('title', 'desc', 'PI', 'PIemail', 'desc', 'startdate', 'enddate', 'project_status', 'initial_contact',
                'dmp_agreed', 'sciSupContact', 'sciSupContact2', 'primary_dataCentre', 'other_dataCentres',
                'status', 'dmp_URL', 'ODMP_URL',)
        widgets = {'startdate': DateInput(), 'enddate': DateInput(), 'dmp_agreed': DateInput(), 'initial_contact': DateInput()}
