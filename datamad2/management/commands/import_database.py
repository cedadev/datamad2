# encoding: utf-8
"""
Import a tab delimited database dump from datamad
"""
__author__ = 'Richard Smith'
__date__ = '04 Mar 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.core.management.base import BaseCommand, CommandError
from datamad2.models import ImportedGrant, Grant

import pandas as pd
import math
from dateutil.parser import parse
from tqdm import tqdm
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal


mapping = {
    'PROJECT_TITLE': 'title',
    'GRANTREFERENCE': 'grant_ref',
    'GRANT_STATUS': 'grant_status',
    'AMOUNT': 'amount_awarded',
    'GRANT_TYPE': 'grant_type',
    'SCHEME': 'scheme',
    'LEAD_GRAN': 'lead_grant',
    'GRANT_HOLDER': 'grant_holder',
    'DEPARTMENT': 'department',
    'RESEARCH_ORG': 'research_org',
    'ADDRESS1': 'address1',
    'ADDRESS2': 'address2',
    'CITY': 'city',
    'POSTCODE': 'post_code',
    'EMAIL': 'email',
    'WORK_NUMBER': 'work_number',
    'ROUTING_CLASSIFICATION': 'routing_classification',
    'SECONDARY_CLASSIFICATION': 'secondary_classification',
    'SCIENCE_AREA': 'science_area',
    'NCAS': 'ncas',
    'NCEO': 'nceo',
    'PROPOSED_ST_DT': 'proposed_start_date',
    'PROPOSED_END_DT': 'proposed_end_date',
    'ACTUAL_START_DATE': 'actual_start_date',
    'ACTUAL_END_DATE': 'actual_end_date',
    'ABSTRACT': 'abstract',
    'OBJECTIVES': 'objectives'
}


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('input_file', help='Tab delimited file to import')

    def handle(self, *args, **options):

        # Load file
        df = pd.read_table(options['input_file'])

        for row in tqdm(df.itertuples(), desc='Importing grants'):
            data = {}

            for source_field, model_field in mapping.items():

                value = getattr(row, source_field)

                # Ignore NaN values
                if not isinstance(value, str) and math.isnan(value):
                    continue

                if source_field in ('LEAD_GRAN', 'NCAS', 'NCEO'):
                    # Turn into boolean
                    value = bool('y' in value.lower())

                elif source_field in ('PROPOSED_ST_DT','PROPOSED_END_DT','ACTUAL_START_DATE','ACTUAL_END_DATE'):
                    # Convert the date
                    value = parse(value, default=None).date()

                elif source_field in ('AMOUNT'):
                    value = Decimal(value).quantize(Decimal('1.00'))

                # Add to the data dict
                data[model_field] = value

            ig = ImportedGrant(**data)

            model_fields = [model_field for source_field, model_field in mapping.items()]
            grant_ref = row.GRANTREFERENCE

            try:
                existing_G = Grant.objects.get(grant_ref=grant_ref)
                existing_ig = existing_G.importedgrant_set.first()
                changed_fields = list(filter(
                    lambda field: getattr(existing_ig, field, None) != getattr(ig, field, None), model_fields))

                if len(changed_fields) > 0:
                    ig.save()

                else:
                    pass

            except ObjectDoesNotExist:
                ig = ImportedGrant(**data)
                ig.save()


        # Attach parent child relationships
        for row in tqdm(df.itertuples(), desc='Making parent child connections'):
            parent_grant = row.PARENT_GRANT
            row_grant = row.GRANTREFERENCE

            # Ignore NaN values
            if not isinstance(parent_grant, str) and math.isnan(parent_grant):
                continue

            try:
                pg = Grant.objects.get(grant_ref=parent_grant)
            except ObjectDoesNotExist:
                print(f'Parent Grant {parent_grant} does not exist.')
                pg = None

            # Get most recent imported grant. Should be the one just imported
            igrant = ImportedGrant.objects.filter(grant_ref=row_grant).first()

            if pg and igrant:
                igrant.parent_grant = pg
                igrant.save()
