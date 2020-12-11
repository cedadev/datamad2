# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '11 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Datamad imports
import datamad2.forms as datamad_forms
from datamad2.models import  DocumentTemplate
from datamad2.views.mixins import DatacentreAdminTestMixin
from datamad2.views.generic import ObjectDeleteView
from datamad2.tables import DocumentTemplateTable

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, CreateView

# Utility imports
from django_tables2.views import SingleTableView


class DocumentTemplateListView(LoginRequiredMixin, DatacentreAdminTestMixin, SingleTableView):
    """
    List of document templates attributed to the current logged in users data centre
    """

    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_list.html'
    table_class = DocumentTemplateTable


class DocumentTemplateCreateView(LoginRequiredMixin, DatacentreAdminTestMixin, CreateView):
    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_form.html'
    form_class = datamad_forms.DocumentTemplateForm

    def get_success_url(self):
        return reverse('document_template_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class DocumentTemplateUpdateView(LoginRequiredMixin, DatacentreAdminTestMixin, UpdateView):
    model = DocumentTemplate
    template_name = 'datamad2/user_account/datacentre_document_template_form.html'
    form_class = datamad_forms.DocumentTemplateForm

    def get_success_url(self):
        return reverse('document_template_list')


class DocumentTemplateDeleteView(ObjectDeleteView):
    model = DocumentTemplate
    success_url = reverse_lazy('document_template_list')