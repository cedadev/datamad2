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
    grant_ref = indexes.CharField(model_attr='grant_ref', faceted=True)
    assigned_datacentre = indexes.CharField(model_attr='assigned_data_centre', null=True, faceted=True, default='Unassigned')
    other_datacentre = indexes.CharField(model_attr='other_data_centre', null=True, faceted=True, default='Unassigned')
    labels = indexes.CharField(model_attr='importedgrant__labels', null=True, faceted=True, default='Unassigned')
    secondary_classification = indexes.CharField(model_attr='importedgrant__secondary_classification', null=True, faceted=True, default='Unassigned')
    grant_status = indexes.CharField(model_attr='importedgrant__grant_status', null=True, faceted=True, default='Unassigned')
    grant_type = indexes.CharField(model_attr='importedgrant__grant_type', null=True, faceted=True, default='Unassigned')
    scheme = indexes.CharField(model_attr='importedgrant__scheme', null=True, faceted=True, default='Unassigned')
    call = indexes.CharField(model_attr='importedgrant__call', null=True, faceted=True, default='Unassigned')
    facility = indexes.CharField(model_attr='importedgrant__facility', null=True, faceted=True, default='Unassigned')
    lead = indexes.CharField(model_attr='importedgrant__lead_grant', null=True, faceted=True)
    ncas = indexes.CharField(model_attr='importedgrant__ncas', null=True, faceted=True)
    nceo = indexes.CharField(model_attr='importedgrant__nceo', null=True, faceted=True)
    overall_score = indexes.IntegerField(model_attr='importedgrant__overall_score', null=True)
    date_added = indexes.DateTimeField(model_attr='importedgrant__creation_date', null=True)
    actual_start_date = indexes.DateField(model_attr='importedgrant__actual_start_date', null=True)
    dmp_agreed = indexes.CharField(model_attr='dmp_agreed', null=True, faceted=True)

    def get_model(self):
        return Grant

    def prepare_secondary_classification(self, obj):
        if not obj.importedgrant:
            return None
        
        secondary_classification = obj.importedgrant.secondary_classification
        if secondary_classification:
            return secondary_classification.split(':')[0]
        return secondary_classification

    def prepare_labels(self, obj):
        if not obj.importedgrant:
            return None
        
        all_labels = obj.importedgrant.labels
        labels = {area.split()[0] for area in all_labels['science_areas']}
        labels.update(
            set(
                all_labels.get('routing_classification',[])
            )
        )

        return list(labels)
