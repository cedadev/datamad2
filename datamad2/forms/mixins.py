# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '01 Oct 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CrispySubmitMixin:
    """
    Adds a save button at the bottom of a crispy rendered form.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Save'))
