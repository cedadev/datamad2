# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '11 Jun 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

import django_tables2 as tables
from .models import Grant, DataProduct
from django_tables2.utils import A


class GrantTable(tables.Table):
    grant_ref = tables.LinkColumn(
        viewname='grant_detail',
        args=[A('pk')],
        verbose_name='Grant Reference'
    )
    labels = tables.TemplateColumn(
        template_name='datamad2/fields/top_categories_field.html'
    )

    date_added = tables.DateTimeColumn(
        accessor='importedgrant__creation_date',
        format='d M Y'
    )

    actual_start_date = tables.DateColumn(
        accessor='importedgrant__actual_start_date',
        format='d M Y'
    )

    assigned_datacentre = tables.TemplateColumn(
        accessor='assigned_data_centre',
        template_name='datamad2/fields/assigned_datacentre_field.html',
        attrs={'td':{'class': 'align-middle text-center'}}
    )

    associated_grants = tables.TemplateColumn(
        template_name='datamad2/fields/associated_grants_field.html'
    )

    grant_title = tables.TemplateColumn(
        template_name='datamad2/fields/grant_title_field.html'
    )

    class Meta:
        model = Grant
        template_name = 'django_tables2/bootstrap-responsive.html'
        attrs = {
            'td': {
                'class': 'align-middle'
            }
        }
        fields = (
            'importedgrant__grant_holder',
        )
        sequence = (
            'grant_ref',
            'grant_title',
            'importedgrant__grant_holder',
            'labels',
            'date_added',
            'actual_start_date',
            'assigned_datacentre',
            '...'
        )


class DataProductTableMixin(tables.Table):
    actions = tables.TemplateColumn(
        template_name='datamad2/fields/data_product_action_field.html'
    )


class DataProductMeta:
    model = DataProduct
    template_name = 'django_tables2/bootstrap-responsive.html'
    orderable = False
    empty_text = "No data products in this category"

    fields = [
        'added',
        'modified',
        'actions'
    ]

    sequence = [
        '...',
        'added',
        'modified',
        'actions'
    ]


class DigitalDataProductTable(DataProductTableMixin, tables.Table):
    class Meta(DataProductMeta):
        fields = [
            'description',
            'contact',
            'data_volume',
            'delivery_date',
            'embargo_date',
            'doi',
            'preservation_plan',
            'additional_comments',
            'data_product_type',
        ] + DataProductMeta.fields


class ModelSourceDataProductTable(DataProductTableMixin):
    class Meta(DataProductMeta):
        fields = [
            'name',
            'contact',
            'description',
            'sample_destination',
            'additional_comments',
        ] + DataProductMeta.fields


class PhysicalDataProductTable(DataProductTableMixin):
    class Meta(DataProductMeta):
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments',
        ] + DataProductMeta.fields


class HardcopyDataProductTable(DataProductTableMixin):
    class Meta(DataProductMeta):
        fields = [
            'name',
            'contact',
            'data_format',
            'issues',
            'delivery_date',
            'additional_comments',
        ] + DataProductMeta.fields


class ThirdPartyDataProductTable(DataProductTableMixin):
    class Meta(DataProductMeta):
        fields = [
            'name',
            'contact',
            'data_location',
            'description',
            'data_volume',
            'responsibility',
            'issues',
            'additional_comments',
            'added',
            'modified',
            'actions'
        ]