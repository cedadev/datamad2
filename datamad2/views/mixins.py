# encoding: utf-8
"""
Custom mixins for the Datamad Application
"""
__author__ = 'Richard Smith'
__date__ = '10 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Django imports
from django.contrib.auth.mixins import UserPassesTestMixin


class UpdateOrCreateMixin:
    """
    Mixin to overwrite the get_object method so this view behaves as an update or create view.
    If the object doesn't exist, it will render a blank form so you can create one.
    """
    def get_object(self, queryset=None):
        """
        Behaves like an update or create view
        """

        # Use a custom queryset if provided; this is required for subclasses
        # like DateDetailView
        if queryset is None:
            queryset = self.get_queryset()

        # Next, try looking up by primary key.
        pk = self.kwargs.get(self.pk_url_kwarg)
        slug = self.kwargs.get(self.slug_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        # Next, try looking up by slug.
        if slug is not None and (pk is None or self.query_pk_and_slug):
            slug_field = self.get_slug_field()
            queryset = queryset.filter(**{slug_field: slug})

        try:
            # Check if there are any query parameters
            # If there are no filters and there is only 1 item in the queryset
            # this mixin will default to return and object even if you are
            # trying to create a new one
            if not slug and not pk:
                return None

            # Get the single item from the filtered queryset
            return queryset.get()

        except queryset.model.DoesNotExist:
            return None


class DatacentreAdminTestMixin(UserPassesTestMixin):
    """
    Checks if the user is an admin
    """

    def test_func(self):
        return self.request.user.is_admin