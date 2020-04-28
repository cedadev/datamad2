# encoding: utf-8
"""
Merge a csv file into datamad
"""

from django.core.management.base import BaseCommand, CommandError
from datamad2.models import ImportedGrant, Grant, DataCentre

import pandas as pd
import math
from dateutil.parser import parse
from tqdm import tqdm
from django.core.exceptions import ObjectDoesNotExist
import numpy as np

# mapping = {
#     'Grant Reference': 'grant_ref',
#     'Title': 'title',
#     'C for S found?': 'case_for_support_found',
#     'Routing Classification': 'routing_classification',
#     'Secondary Classifications': 'secondary_classification',
#     'Assigned Data Centre': 'assigned_data_centre',
#     'Comments': 'comments',
#     'Grant Holder': 'grant_holder',
#     'Research Organisation': 'research_org',
#     'Grant Status': 'grant_status',
#     'Parent Grant': 'parent_grant',
#     'Lead Grant (Yes / No)': 'lead_grant',
#     'AmountAwarded': 'amount_awarded',
#     'Science Area': 'science_area',
#     # 'Geographic Area',
#     'Other DC\'s Expecting Datasets': 'other_data_centre',
#     'Scheme': 'scheme',
#     # 'Call',
#     'Grant Type': 'grant_type',
#     'E-Mail': 'email',
#     'Work Number': 'work_number',
#     'NCAS (Yes/No)': 'ncas',
#     'NCEO (yes/No)': 'nceo',
#     'Actual Start Date': 'actual_start_date',
#     'Actual End Date': 'actual_end_date',
#     'Proposed Start date': 'proposed_start_date',
#     'Proposed End date': 'proposed_end_date',
#     'Will Grant Produce Data': 'will_grant_produce_data',
#     'DateContact with PI': 'date_contacted_pi',
#     # 'Full DMP Agreed':,
#     # 'Date DMP signoff',
#     'Department': 'department',
#     'City': 'city',
#     'Address 2': 'address2',
#     'Address 1': 'address1',
#     'Post Code': 'post_code',
#     # 'End Date Changed?':,
#     # 'Start Date Changed?',
#     'Hide Record': 'hide_record',
#     #'Move hidden grants to archive list',
#     #'Move hidden grants to archive list2',
#     #'Move items to archive list',
#     #'Facility',
#     #'Facility1',
#     'Abstract': 'abstract',
#     'Alt Data Contact' : 'alt_data_contact',
#     'Alt Data Contact Email': 'alt_data_contact_email',
#     'Alt Data Contact Phone No': 'alt_data_contact_phone',
#     #'App Created By',
#     #'App Modified By',
#     #'Are materials coming to NGR',
#     #'BGS contact',
#     #'Compliance Asset Id',
#     #'Content Type',
#     #'Created',
#     #'Created By',
#     'Data Contact' : 'data_contact',
#     'Data Contact Email': 'data_contact_email',
#     'Data Contact Phone': 'data_contact_phone',
#     'Datasets Delivered as per DMP?': 'datasets_delivered',
#     #'Date large data expected':'',
#     #'Date NGR notified of physical materials',
#     #'Date physical material deposited at NGR',
#     #'Detailed Accession Item ID',
#     #'DMP refers to physical materials',
#     #'DOI',
#     #'Folder Child Count',
#     #'Grant approved date',
#     #'ID',
#     #'Item Child Count',
#     #'Label applied by',
#     #'Label setting',
#     #'Large data expected (in TB)',
#     #'LargeTicketItemCost',
#     #'LargeTicketItemDescrition',
#     # 'Metadata_dataident_id',
#     # 'Modified',
#     # 'Modified By',
#     # 'NGDC Correspondence',
#     # 'NGDC Correspondence Archive',
#     # 'NGDC date to contact',
#     # 'NGDC DMP Documents',
#     # 'NGDC Grants Round Category',
#     # 'NGDC Notes',
#     # 'NGDC partial data received',
#     'Objectives': 'objectives',
#     #'OK to archive',
#     #'Original Proposed End Date',
#     #'Original Proposed Start Date',
#     #'Overall Score',
#     #'Project Title',
#     #'Reason to contact',
#     #'Retention label',
#     #'Retention label Applied',
#     'Sanctions Recommended': 'sanctions_recommended',
#     #'Target Audiences',
#     #'Item Type',
#     #'Path'
# }

mapping = {
    'grant_reference': 'grant_ref',
    'title': 'title',
    'c_for_s_found': 'case_for_support_found',
    'routing_classification': 'routing_classification',
    'secondary_classifications': 'secondary_classification',
    'assigned_data_centre': 'assigned_data_centre',
    'comments': 'comments',
    'grant_holder': 'grant_holder',
    'research_organisation': 'research_org',
    'grant_status': 'grant_status',
    'parent_grant': 'parent_grant',
    'lead_grant_yes___no': 'lead_grant',
    'amountawarded': 'amount_awarded',
    'science_area': 'science_area',
    'other_dcs_expecting_datasets': 'other_data_centre',
    'scheme': 'scheme',
    'grant_type': 'grant_type',
    'email': 'email',
    'work_number': 'work_number',
    'ncas_yes_no': 'ncas',
    'nceo_yes_no': 'nceo',
    'actual_start_date': 'actual_start_date',
    'actual_end_date': 'actual_end_date',
    'proposed_start_date': 'proposed_start_date',
    'proposed_end_date': 'proposed_end_date',
    'will_grant_produce_data': 'will_grant_produce_data',
    'datecontact_with_pi': 'date_contacted_pi',
    'department': 'department',
    'city': 'city',
    'address_2': 'address2',
    'address_1': 'address1',
    'post_code': 'post_code',
    'hide_record': 'hide_record',
    'abstract': 'abstract',
    'alt_data_contact_email': 'alt_data_contact_email',
    'alt_data_contact_phone_no': 'alt_data_contact_phone',
    'data_contact_email': 'data_contact_email',
    'data_contact_phone': 'data_contact_phone',
    'datasets_delivered_as_per_dmp': 'datasets_delivered',
    'objectives': 'objectives',
    'sanctions_recommended': 'sanctions_recommended',
}

cols = [
    'Grant Reference',
    'Title',
    'C for S found?',
    'Routing Classification',
    'Secondary Classifications',
    'Assigned Data Centre',
    'Comments',
    'Grant Holder',
    'Research Organisation',
    'Grant Status',
    'Parent Grant',
    'Lead Grant (Yes / No)',
    'AmountAwarded',
    'Science Area',
    'Geographic Area',
    'Other DC\'s Expecting Datasets',
    'Scheme',
    'Call',
    'Grant Type',
    'E-Mail',
    'Work Number',
    'NCAS (Yes/No)',
    'NCEO (yes/No)',
    'Actual Start Date',
    'Actual End Date',
    'Proposed Start date',
    'Proposed End date',
    'Will Grant Produce Data',
    'DateContact with PI',
    'Full DMP Agreed',
    'Date DMP signoff',
    'Department',
    'City',
    'Address 2',
    'Address 1',
    'Post Code',
    'End Date Changed?',
    'Start Date Changed?',
    'Hide Record',
    'Move hidden grants to archive list',
    'Move hidden grants to archive list2',
    'Move items to archive list',
    'Facility',
    'Facility1',
    'Abstract',
    'Alt Data Contact',
    'Alt Data Contact Email',
    'Alt Data Contact Phone No',
    'App Created By',
    'App Modified By',
    'Are materials coming to NGR',
    'BGS contact',
    'Compliance Asset Id',
    'Content Type',
    'Created',
    'Created By',
    'Data Contact',
    'Data Contact Email',
    'Data Contact Phone',
    'Datasets Delivered as per DMP?',
    'Date large data expected',
    'Date NGR notified of physical materials',
    'Date physical material deposited at NGR',
    'Detailed Accession Item ID',
    'DMP refers to physical materials',
    'DOI',
    'Folder Child Count',
    'Grant approved date',
    'ID',
    'Item Child Count',
    'Label applied by',
    'Label setting',
    'Large data expected (in TB)',
    'LargeTicketItemCost',
    'LargeTicketItemDescrition',
    'Metadata_dataident_id',
    'Modified',
    'Modified By',
    'NGDC Correspondence',
    'NGDC Correspondence Archive',
    'NGDC date to contact',
    'NGDC DMP Documents',
    'NGDC Grants Round Category',
    'NGDC Notes',
    'NGDC partial data received',
    'Objectives',
    'OK to archive',
    'Original Proposed End Date',
    'Original Proposed Start Date',
    'Overall Score',
    'Project Title',
    'Reason to contact',
    'Retention label',
    'Retention label Applied',
    'Sanctions Recommended',
    'Target Audiences',
    'Item Type',
    'Path'
]

boolean_fields = ('hide_record',
                  'will_grant_produce_data',
                  'datasets_delivered',
                  'sanctions_recommended',
                  'case_for_support_found',
                  'lead_grant',
                  'ncas',
                  'nceo')

date_fields = ('date_contacted_pi',
               'proposed_start_date',
               'proposed_end_date',
               'actual_start_date',
               'actual_end_date')

grant_fields = ('grant_ref',
                'alt_data_contact',
                'alt_data_contact_email',
                'alt_data_contact_phone',
                'assigned_data_centre',
                'other_data_centre',
                'hide_record',
                'date_contacted_pi',
                'will_grant_produce_data',
                'datasets_delivered',
                'sanctions_recommended',
                'case_for_support_found')

imported_grant_fields = ('grant_ref',
                         'title',
                         'routing_classification',
                         'secondary_classification',
                         'comments',
                         'grant_holder',
                         'research_org',
                         'grant_status',
                         'parent_grant',
                         'lead_grant',
                         'amount_awarded',
                         'science_area',
                         'scheme',
                         'grant_type',
                         'email',
                         'work_number',
                         'ncas',
                         'nceo',
                         'actual_start_date',
                         'actual_end_date',
                         'proposed_start_date',
                         'proposed_end_date',
                         'department',
                         'city',
                         'address2',
                         'address1',
                         'post_code',
                         'abstract',
                         'objectives',
                         'data_contact',
                         'data_contact_email',
                         'data_contact_phone',
                         )



class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('input_file', help='CSV file to merge')

    def handle(self, *args, **options):

        # Load file
        df = pd.read_csv(options['input_file'], header=0, skipinitialspace=True)

        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '')\
            .str.replace(')', '').str.replace('?', '').str.replace('/', '_').str.replace('\'', '')\
            .str.replace('-', '')

        for row in tqdm(df.itertuples(), desc='Adding grant info'):
            g_data = {}

            for source_field, model_field in mapping.items():
                if model_field in grant_fields:
                    value = row.__getattribute__(source_field)

                    if model_field in ['assigned_data_centre', 'other_data_centre']:
                        try:
                            value = DataCentre.objects.get(name=value)
                        except Exception as exc:
                            value = None

                    if model_field in date_fields:
                        # Convert the date
                        try:
                            value = parse(value)
                            value = value.strftime('%Y-%m-%d')
                        except Exception as exc:
                            value = None

                    if model_field in boolean_fields:
                        # Turn into boolean
                        if value == 'Yes':
                            value = True
                        elif value == 'No':
                            value = False
                        else:
                            value = None

                    if isinstance(value, float) and np.isnan(value):
                        value = None

                    # Add to the data dict
                    g_data[model_field] = value

            grant_ref = row[1]
            g = Grant.objects.filter(grant_ref=grant_ref)
            g.update(**g_data)


        # Add grant to imported grant
        for row in tqdm(df.itertuples(), desc='Linking grant and imported grant'):
            grant_ref = row[1]

            try:
                g = Grant.objects.get(grant_ref=grant_ref)

            except ObjectDoesNotExist:
                print(f'Grant with grant ref {grant_ref} does not exist.')
                continue

            igrant = ImportedGrant.objects.filter(grant_ref=grant_ref).first()

            if g and igrant:
                igrant.grant = g
                igrant.save()
                g.save()
