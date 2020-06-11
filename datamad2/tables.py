# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '11 Jun 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import django_tables2 as tables
from .models import Grant
from django_tables2.utils import A


class GrantTable(tables.Table):
    grant_ref = tables.LinkColumn(viewname='grant_detail', args=[A('importedgrant__pk')], verbose_name='Grant Reference')
    routing_classification = tables.TemplateColumn(template_name='datamad2/fields/routing_classification_field.html')
    date_added = tables.DateTimeColumn(accessor='importedgrant__creation_date', format='d M Y')
    claim_status = tables.TemplateColumn(accessor='claimed', template_name='datamad2/fields/claim_status_field.html', attrs={'td':{'class': 'align-middle text-center'}})

    class Meta:
        model = Grant
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {
            'td': {
                'class': 'align-middle'
            }
        }
        fields = (
            'importedgrant__title',
            'importedgrant__grant_holder',
        )
        sequence = (
            'grant_ref',
            'importedgrant__title',
            'importedgrant__grant_holder',
            'routing_classification',
            'date_added',
            'claim_status',
            '...'
        )


class DataCentreGrantTable(GrantTable):

    class Meta(GrantTable.Meta):
        exclude=('claim_status',)
