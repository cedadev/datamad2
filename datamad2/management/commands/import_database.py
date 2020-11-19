# encoding: utf-8
"""
Import a tab delimited database dump from datamad
"""
__author__ = 'Richard Smith'
__date__ = '04 Mar 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.core.management.base import BaseCommand
from datamad2.models import ImportedGrant, Grant

import pandas as pd
import math
from dateutil.parser import parse
from tqdm import tqdm
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import io
import requests
from requests.auth import HTTPBasicAuth

mapping = {
    'GRANTREFERENCE': 'grant_ref',
    'PROJECT_TITLE': 'title',
    'SCHEME': 'scheme',
    'CALL': 'call',
    'GRANT_TYPE': 'grant_type',
    'GRANT_HOLDER': 'grant_holder',
    'WORK_NUMBER': 'work_number',
    'EMAIL': 'email',
    'RESEARCH_ORG': 'research_org',
    'DEPARTMENT': 'department',
    'ACTUAL_START_DATE': 'actual_start_date',
    'ACTUAL_END_DATE': 'actual_end_date',
    'NCAS': 'ncas',
    'NCEO': 'nceo',
    'PROPOSED_ST_DT': 'proposed_start_date',
    'PROPOSED_END_DT': 'proposed_end_date',
    'GRANT_STATUS': 'grant_status',
    'ADDRESS1': 'address1',
    'ADDRESS2': 'address2',
    'CITY': 'city',
    'POSTCODE': 'post_code',
    'LEAD_GRANT': 'lead_grant',
    'AMOUNT': 'amount_awarded',
    'ROUTING_CLASSIFICATION': 'routing_classification',
    'SCIENCE_AREA': 'science_area',
    'SECONDARY_CLASSIFICATION': 'secondary_classification',
    'ABSTRACT': 'abstract',
    'OBJECTIVES': 'objectives',
    'FACILITY': 'facility',
    'OVERALL_SCORE': 'overall_score'
}


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        input_group = parser.add_mutually_exclusive_group()
        input_group.add_argument('--url', help='Import database from URL')
        input_group.add_argument('--file', help='CSV file to import')
        parser.add_argument('--username')
        parser.add_argument('--password')

    def handle(self, *args, **options):

        if options.get('url'):
            r = requests.get(
                options['url'],
                auth=HTTPBasicAuth(
                    options.get('username'),
                    options.get('password')
                )
            )

            if r.text[:15] == '"GRANTREFERENCE':
                database_input = io.StringIO(r.text)
        else:
            database_input = options.get('file')

        # Load file
        df = pd.read_csv(database_input)

        for row in tqdm(df.itertuples(), desc='Importing grants'):
            data = {}

            for source_field, model_field in mapping.items():

                value = getattr(row, source_field)

                # Ignore NaN values
                if not isinstance(value, str) and math.isnan(value):
                    continue

                if source_field in ('LEAD_GRANT', 'NCAS', 'NCEO'):
                    # Turn into boolean
                    value = bool('y' in value.lower())

                elif source_field in ('PROPOSED_ST_DT', 'PROPOSED_END_DT', 'ACTUAL_START_DATE', 'ACTUAL_END_DATE'):
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
                existing_ig = existing_G.importedgrant
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

            # unlink parent/ child grants from older imported grants
            for ig in ImportedGrant.objects.filter(grant_ref=row_grant):
                ig.parent_grant = None

            # Get most recent imported grant. Should be the one just imported
            igrant = ImportedGrant.objects.filter(grant_ref=row_grant).first()

            if pg and igrant:
                igrant.parent_grant = pg
                igrant.save()
