# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '11 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Datamad imports
from datamad2.multiforms import MultiFormsView
import datamad2.forms as datamad_forms
from datamad2.models import User
from datamad2.views.mixins import DatacentreAdminTestMixin
from datamad2.tables import UserTable
from datamad2.views.generic import ObjectDeleteView

# Django imports
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import UpdateView, CreateView
from django.views.generic import TemplateView
from django.contrib import messages

# Utility imports
from django_tables2.views import SingleTableView


class MyAccountDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'datamad2/user_account/my_account.html'


class MyAccountPreferencesView(LoginRequiredMixin, MultiFormsView):
    template_name = 'datamad2/user_account/account_preferences.html'
    form_classes = {'facets': datamad_forms.FacetPreferencesForm,
                    'sort_by': datamad_forms.SortByPreferencesForm}
    success_url = reverse_lazy('preferences')

    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)

    def get_facets_initial(self):
        initial = {}
        preferred_facets = self.request.user.preferences.get('preferred_facets', [])
        for facet in preferred_facets:
            initial[facet] = True
        return initial

    def get_sort_by_initial(self):
        initial = {}
        sorting = self.request.user.preferences.get('preferred_sorting', None)
        initial['sort_by'] = sorting
        return initial

    def facets_form_valid(self, form):
        preferences = [field for field, value in form.cleaned_data.items() if value]
        user = User.objects.get(pk=self.request.user.pk)
        user.preferred_facets = ','.join(preferences)
        user.save()

    def sort_by_form_valid(self, form):
        preference = [value for field, value in form.cleaned_data.items() if value]
        user = User.objects.get(pk=self.request.user.pk)
        if preference:
            user.preferred_sorting = preference[0]
        else:
            user.preferred_sorting = None
        user.save()


class MyAccountUsersView(LoginRequiredMixin, SingleTableView):
    template_name = 'datamad2/user_account/datacentre_users.html'
    model = User
    table_class = UserTable

    def get_queryset(self):
        """
        Filter user list just to show users from the admins datacentre
        :return:
        """
        return User.objects.filter(data_centre=self.request.user.data_centre)


class MyAccountNewUserView(LoginRequiredMixin, DatacentreAdminTestMixin, CreateView):
    template_name = 'datamad2/user_account/datacentre_new_users.html'
    model = User
    form_class = datamad_forms.NewUserForm

    def get_success_url(self):
        messages.success(self.request, 'User added successfully')
        return reverse('user_list')

    def get_initial(self):
        initial = super().get_initial()
        if not self.object:
            initial.update({
                'data_centre': self.request.user.data_centre
            })
        return initial


class MyAccountEditUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'datamad2/user_account/datacentre_edit_user.html'
    model = User
    form_class = datamad_forms.UserEditForm

    def test_func(self):
        return self.request.user.is_admin or self.request.user.pk == self.kwargs['pk']

    def get_success_url(self):
        messages.success(self.request, 'User updated successfully')
        return reverse('user_list')


class MyAccountRemoveUserView(DatacentreAdminTestMixin, ObjectDeleteView):
    model = User

    def get_success_url(self):
        messages.success(self.request, 'User deleted successfully')
        return reverse('user_list')