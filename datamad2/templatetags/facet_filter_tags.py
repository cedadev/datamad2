# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '27 Jul 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from datamad2.search_indexes import ImportedGrantIndex
from django import template
from datamad2.utils import removesuffix
from django.template.loader import get_template

register = template.Library()


@register.simple_tag
def available_facets(request):
    """
    Return the available facets which have not been set as preferences
    :param request:
    :return:
    """
    igx = ImportedGrantIndex()

    fields = [removesuffix(field, '_exact') for field in igx.field_map if field.endswith('_exact')]
    preferences = request.user.preferences
    facet_preferences = preferences.get('prefered_facets',[])
    avail_facets = []
    for field in fields:
        if field not in facet_preferences:
            avail_facets.append(field)

    return [field for field in fields if field not in facet_preferences]


@register.simple_tag(takes_context=True)
def selected_facets(context):
    request = context.request
    selected_facets = request.GET.getlist('selected_facets')
    converted_facets = {}

    for facet in selected_facets:
        f, label = facet.split(':')
        title = f.replace('_', ' ').title()
        converted_facets[title]=label

    if converted_facets:
        template = get_template('datamad2/includes/selected_facets.html')
        return template.render({'converted_facets': converted_facets})
