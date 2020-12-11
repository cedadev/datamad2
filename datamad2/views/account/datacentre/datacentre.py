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
from datamad2.models import DataCentre

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404


class MyAccountDatacentreView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Displays basic information about the Datacentre. Page only show to admins

    """
    template_name = 'datamad2/user_account/account_datacentre.html'
    model = DataCentre
    form_class = datamad_forms.DatacentreForm

    def test_func(self):
        return self.request.user.is_admin

    def get_success_url(self):
        return reverse('datacentre')

    def get_object(self, **kwargs):
        """
        Overwrite the get_object method to only display the datacentre object for
        the current logged in user
        :param kwargs:
        :return: The current users datacentre
        """
        return get_object_or_404(self.model, pk=self.request.user.data_centre.pk)