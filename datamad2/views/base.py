# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '10 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Datamad imports
import datamad2.forms as datamad_forms
from datamad2.tables import DigitalDataProductTable, ModelSourceDataProductTable, \
    PhysicalDataProductTable, HardcopyDataProductTable, ThirdPartyDataProductTable

DATAPRODUCT_FORM_CLASS_MAP = {
    'digital': datamad_forms.DigitalDataProductForm,
    'model_source': datamad_forms.ModelSourceDataProductForm,
    'physical': datamad_forms.PhysicalDataProductForm,
    'hardcopy': datamad_forms.HardcopyDataProductForm,
    'third_party': datamad_forms.ThirdPartyDataProductForm
}

DATAPRODUCT_TABLE_CLASS_MAP = {
    'digital': DigitalDataProductTable,
    'model_source': ModelSourceDataProductTable,
    'physical': PhysicalDataProductTable,
    'hardcopy': HardcopyDataProductTable,
    'third_party': ThirdPartyDataProductTable
}
