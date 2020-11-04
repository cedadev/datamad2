# encoding: utf-8
"""
Import Documents from a directory and upload to datamad. Shortcuts the web
front end.

Usage:

python manage.py import_documents <DIRECTORY_CONTAINING_DOCUMENTS>
"""
__author__ = 'Richard Smith'
__date__ = '03 Nov 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


from django.core.management.base import BaseCommand
from datamad2.views import DOCUMENT_NAMING_PATTERN
from datamad2.models import Grant, Document
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.files import File

from pathlib import Path
from tqdm import tqdm


class Command(BaseCommand):
    help = __doc__

    def add_arguments(self, parser):
        parser.add_argument('source_directory')

    def handle(self, *args, **options):

        source_dir = Path(options['source_directory'])

        files = source_dir.glob('*')

        for file in tqdm(files):

            # Check item is a file
            if not file.is_file():
                continue

            # Compare against the naming convention
            try:
                m = DOCUMENT_NAMING_PATTERN.match(file.name)
                if not m:
                    print(f"{file.name} - File name does not match convention. e.g NE_G0123X_1_DMP.docx")
                    continue

                grant_ref = m.group('grant_ref').replace('_','/')

                # Extract the doc type
                file_type = m.group('doc_type').lower()
                if file_type != 'dmp':
                    file_type = 'support'

                # Upload file
                with open(file.absolute(), 'rb') as reader:
                    doc_file = File(reader)
                    doc_file.name = file.name
                    document = Document(upload=doc_file)

                    document.grant = Grant.objects.get(grant_ref=grant_ref)
                    document.type = file_type
                    document.save()

            except ValidationError:
                print(f'File already uploaded for {grant_ref}')

            except ObjectDoesNotExist:
                print(f'Grant not found: {grant_ref}')
