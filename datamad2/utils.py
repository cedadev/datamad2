# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '29 Jul 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from docxtpl import DocxTemplate
from django.conf import settings
import os
from datetime import datetime
import functools


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


def generate_document_from_template(template, context):
    doc = DocxTemplate(template.template.path)
    doc.render(context)
    # checksum = md5(doc.read()).hexdigest()

    # Make sure the destination path exists
    if not os.path.exists(f'{settings.MEDIA_ROOT}/generated_documents'):
        os.mkdir(f'{settings.MEDIA_ROOT}/generated_documents')

    filepath = f'{settings.MEDIA_ROOT}/generated_documents/{template.name.replace(" ","_")}_{datetime.now().strftime("%Y%m%d%h%M%S%f")}.docx'
    doc.save(filepath)

    return filepath


def rgetattr(obj, attr, *args):
    """
    Recursive getattr. Handles dotted attr strings
    :param obj: Original object
    :param attr: attribute to check for. Can be dotted for nested objects
    :param args: see python getattr
    :return: attr or default
    """
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    return functools.reduce(_getattr, [obj] + attr.split('.'))