# encoding: utf-8
"""
Collection of views pertaining to the Preservation Plan Model
"""
__author__ = 'Richard Smith'
__date__ = '11 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


# Datamad imports
import datamad2.forms as datamad_forms
from datamad2.models import PreservationPlan
from datamad2.views.mixins import UpdateOrCreateMixin
from datamad2.tables import PreservationPlanTable
from datamad2.views.generic import ObjectDeleteView

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView

# Utility imports
from django_tables2.views import SingleTableView


class PreservationPlanListView(LoginRequiredMixin, SingleTableView):
    """
    List the preservation plans linked to the user's datacentre
    """
    model = PreservationPlan
    template_name = 'datamad2/user_account/preservation_plan_list.html'
    table_class = PreservationPlanTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs.filter(datacentre=self.request.user.data_centre)

        return qs


class PreservationPlanUpdateCreateView(LoginRequiredMixin, UpdateOrCreateMixin, UpdateView):
    """
    Update or create view for preservation plans.
    If there is not an object with the specified ID it will create one, otherwise
    open form to update.

    Defaults to use the users datacentre in the form
    """
    model = PreservationPlan
    template_name = 'datamad2/user_account/preservation_plan_form.html'
    form_class = datamad_forms.PreservationPlanForm
    success_url = reverse_lazy('preservation_plan_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'datacentre': self.request.user.data_centre
            })
        return initial


class PreservationPlanDeleteView(ObjectDeleteView):
    """
    Preservation plan delete view. Gives a confirmation screen
    """

    model = PreservationPlan
    success_url = reverse_lazy('preservation_plan_list')

