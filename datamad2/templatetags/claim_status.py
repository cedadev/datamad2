# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '24 Mar 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def claim_status(value):
    """
    Filter to return the correct string based on the claim status of the grant
    :param value:
    :return:
    """
    if value:
        return 'Unclaim'

    return 'Claim'
