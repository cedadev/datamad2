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
from datamad2.models import DataFormat
from datamad2.views.mixins import UpdateOrCreateMixin
from datamad2.tables import  DataFormatTable
from datamad2.views.generic import ObjectDeleteView

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

# Utility imports
from django_tables2.views import SingleTableView


class DataFormatListView(LoginRequiredMixin, SingleTableView):
    """
    List all the Data formats attributed to the current users data centre
    """
    model = DataFormat
    template_name = 'datamad2/user_account/data_format_list.html'
    table_class = DataFormatTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(datacentre=self.request.user.data_centre)
        return qs


class DataFormatUpdateCreateView(LoginRequiredMixin, UpdateOrCreateMixin, UpdateView):
    """
    Data Format Update or Create view. If an object with the specified ID exists,
    it opens and edit form, otherwise creation form.

    Form is autofilled with creators Data Centre
    """
    model = DataFormat
    template_name = 'datamad2/user_account/data_format_form.html'
    form_class = datamad_forms.DataFormatForm
    success_url = reverse_lazy('data_format_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class DataFormatDeleteView(ObjectDeleteView):
    """
    Delete the given data format object
    """
    model = DataFormat
    success_url = reverse_lazy('data_format_list')
