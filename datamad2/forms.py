from django import forms
from .models.grants import Grant
from haystack.forms import FacetedSearchForm
from crispy_forms.helper import FormHelper
from .models.document_store import Document


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


class DatamadFacetedSearchForm(FacetedSearchForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method='get'
        self.helper.form_class='ml-0'

    def no_query_found(self):
        """
        Determines the behavior when no query was found.

        By default, no results are returned (``EmptySearchQuerySet``).

        Should you want to show all results, override this method in your
        own ``SearchForm`` subclass and do ``return self.searchqueryset.all()``.
        """
        return self.searchqueryset.all()


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ('upload', 'title',)


class MultipleDocumentUploadForm(forms.Form):
    class Meta:
        model = Document
        fields = ('title', 'upload',)

    upload = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}))
