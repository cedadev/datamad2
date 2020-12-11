# encoding: utf-8
"""
Custom views for the DataMAD application
"""
__author__ = 'Richard Smith'
__date__ = '10 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


# Django Imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import DeleteView


class ObjectDeleteView(LoginRequiredMixin, DeleteView):
    """
    Class based view to provide a delete via a GET call
    """
    template_name = 'datamad2/confirm_delete.html'