from django import forms
from .models.grants import Grant
from haystack.forms import FacetedSearchForm
from crispy_forms.helper import FormHelper
from .models.document_store import Document
from datamad2.search_indexes import ImportedGrantIndex
from crispy_forms.layout import Submit
from .utils import removesuffix
from datamad2.models.users import DataCentre
from bootstrap_datepicker_plus import DatePickerInput


class UpdateClaim(forms.ModelForm):
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
            'case_for_support_found',
            'dmp_agreed'
        )
        widgets = {'date_contacted_pi': DateInput()}


class DatamadFacetedSearchForm(FacetedSearchForm):
    CHOICES = (
        (None, 'Relevance'),
        ('date_added', 'Date Added (asc)'),
        ('-date_added', 'Date Added (desc)'),
        ('actual_start_date', 'Start Date (asc)'),
        ('-actual_start_date', 'Start Date (desc)'),
        ('grant_ref_exact', 'Grant Ref (A-Z)'),
        ('-grant_ref_exact', 'Grant Ref (Z-A)'),
        ('grant_title_exact', 'Grant Title (A-Z)'),
        ('-grant_title_exact', 'Grant Title (Z-A)'),
        ('grant_holder_exact', 'Grant Holder (A-Z)'),
        ('-grant_holder_exact', 'Grant Holder (Z-A)'),
    )
    sort_by = forms.ChoiceField(
        choices=CHOICES,
        required=False,
        widget=forms.Select(attrs={"onchange": "trigger_submit(this)"})
    )

    start_date = forms.DateField(
        required=False,
        label='Start Date Beginning',
        widget=DatePickerInput(options={
            'format': 'DD/MM/YYYY'
        })
    )

    end_date = forms.DateField(
        required=False,
        label='Start Date End',
        widget=DatePickerInput(options={
            'format': 'DD/MM/YYYY'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset.all()

    def search(self):
        sqs = super().search()

        if self.cleaned_data['sort_by']:
            order = self.cleaned_data['sort_by']
            sqs = sqs.order_by(order)

        if self.cleaned_data['start_date']:
            sqs = sqs.filter(acutal_start_date__gte=self.cleaned_data['start_date'])

        if self.cleaned_data['end_date']:
            sqs = sqs.filter(acutal_start_date__lte=self.cleaned_data['end_date'])

        return sqs


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload', 'tags')


class MultipleDocumentUploadForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('upload',)

    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))


class FacetPreferencesForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Update Preferences'))

        igx = ImportedGrantIndex()
        preference_fields = [removesuffix(field, '_exact') for field in igx.field_map if field.endswith('_exact')]

        for field in preference_fields:
            self.fields[field] = forms.BooleanField(required=False)


class DatacentreForm(forms.ModelForm):
    class Meta:
        model = DataCentre
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))
