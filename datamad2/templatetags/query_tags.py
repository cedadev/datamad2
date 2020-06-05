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


@register.simple_tag
def url_replace(request, field, value):
    """ Add/replace a GET parameter in the current URL """

    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()