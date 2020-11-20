# encoding: utf-8
"""
Command to set the creation date of the grants on database initialisation

Usage:

python manage.py set_date_added <INPUT_CSV_FILE>
"""
__author__ = 'Richard Smith'
__date__ = '20 Nov 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Python Imports
from dateutil.parser import parse
from tqdm import tqdm

# Django Imports
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist

# Datamad Imports
from .utils.load_sharepoint_csv import load_sharepoint_csv
from datamad2.models import Grant


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('input_file', help='CSV file to merge')

    def handle(self, *args, **options):
        # Load file
        df = load_sharepoint_csv(options['input_file'])

        for row in tqdm(df.itertuples(), desc='Updating creation dates'):
            created_date = row.__getattribute__('created')

            try:
                created_date = parse(created_date)
                created_date = created_date.strftime('%Y-%m-%d')
            except Exception:
                created_date = None

            grant_ref = row.__getattribute__('grant_reference')

            try:
                g = Grant.objects.get(grant_ref=grant_ref)
                g.date_added = created_date
                g.save()

            except ObjectDoesNotExist:
                continue





