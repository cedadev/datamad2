# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '05 Jun 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django import template

register = template.Library()


@register.filter
def facet_title(value):
    facet = value.replace('_', ' ')
    return facet.title()


@register.filter
def get_item(dictionary, key):
    if not isinstance(dictionary, dict):
        return
    return dictionary.get(key)