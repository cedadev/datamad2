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
def split_pages(page_range, current_page_number):
    """ Converts a range of pages to a truncated list to save room """

    pages = []

    previous_pages = page_range[:current_page_number-1]
    if len(previous_pages) > 4:
        previous_pages = list(previous_pages[-4:])
    else:
        previous_pages = list(previous_pages)

    next_pages = page_range[current_page_number:]
    if len(next_pages) > 4:
        next_pages = list(next_pages[:4])
    else:
        next_pages = list(next_pages)

    pages += previous_pages
    pages.append(current_page_number)
    pages += next_pages
    return pages


@register.simple_tag
def current_results(page_object):
    """ Converts a range of pages to a truncated list to save room """
    current_page = page_object.number
    page_size = page_object.paginator.per_page
    total = page_object.paginator.count
    to_size = (current_page*page_size) if total > (current_page*page_size) else total
    return f"Showing {(current_page-1) * page_size} - {to_size} of {total} results"