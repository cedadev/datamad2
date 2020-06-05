# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '14 May 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from datamad2.models.grants import Grant
from haystack import indexes


class ImportedGrantIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    assigned_datacentre = indexes.CharField(model_attr='assigned_data_centre', null=True, faceted=True, default='Unassigned')
    other_datacentre = indexes.CharField(model_attr='other_data_centre', null=True, faceted=True, default='Unassigned')
    routing_classification = indexes.CharField(model_attr='importedgrant__routing_classification', null=True, faceted=True, default='Unassigned')
    secondary_classification= indexes.CharField(model_attr='importedgrant__secondary_classification', null=True, faceted=True, default='Unassigned')

    def get_model(self):
        return Grant

    def prepare_routing_classification(self, object):
        ig = object.importedgrant_set.first()
        return ig.routing_classification

    def prepare_secondary_classification(self, object):
        ig = object.importedgrant_set.first()
        return ig.secondary_classification

