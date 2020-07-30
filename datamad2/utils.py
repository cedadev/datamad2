# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '29 Jul 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


def removesuffix(text, suffix):
    """
    Remove the suffix from a string
    :param text: base string
    :param suffix: suffix to remove
    :return: string with suffix removed
    """
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    else:
        return text
