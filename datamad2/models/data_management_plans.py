# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '24 Sep 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.db import models
from .grants import Grant
from .users import DataCentre
from .document_store import MediaFileSystemStorage
import os
from sizefield.models import FileSizeField
import hashlib

DOCUMENT_TYPES = (
    ('dmp', 'DMP'),
    ('odmp', 'ODMP'),
    ('cfs', 'CFS'),
    ('ta', 'TA'),
    ('jor', 'JOR'),
    ('proforma', 'PROFORMA')
)


def file_name(instance, filename):
    h = instance.checksum
    datacentre = instance.datacentre.name
    basename, ext = os.path.splitext(filename)
    return os.path.join('document_templates', datacentre, f'{h}{ext}')


class DocumentTemplate(models.Model):
    datacentre = models.ForeignKey(DataCentre, on_delete=models.CASCADE)
    template = models.FileField(upload_to=file_name, storage=MediaFileSystemStorage())
    name = models.CharField(max_length=100, blank=True, help_text='Name will default to mach uploaded file')
    description = models.TextField(blank=True,
                                   help_text="Short description to help other users understand what the template is used for")
    type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)

    def _generate_checksum(self):
        """
        Generate an MD5 checksum to check for file changes
        """
        md5 = hashlib.md5()
        for chunk in self.template.chunks():
            md5.update(chunk)
        self.checksum = md5.hexdigest()

    def save(self, *args, **kwargs):
        """
        Default name to be the same as the uploaded file
        :param args:
        :param kwargs:
        :return:
        """
        self._generate_checksum()

        if not self.name:
            self.name = self.template.name

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} - {self.description}'


class DataFormat(models.Model):
    datacentre = models.ForeignKey(DataCentre, on_delete=models.CASCADE)
    format = models.CharField(max_length=50)

    def __str__(self):
        return self.format


class PreservationPlan(models.Model):
    datacentre = models.ForeignKey(DataCentre, on_delete=models.CASCADE)
    short_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.description}'


class DataProduct(models.Model):
    CHOICES = (
        ('digital', 'Digital Dataset'),
        ('model_source', 'Model Source Code'),
        ('physical', 'Pysical Collections & Samples'),
        ('hardcopy', 'Hardcopy Records'),
        ('third_party', 'Third Party/Existing Datasets'),
    )
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    added = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    data_product_type = models.CharField(choices=CHOICES, max_length=50)

    name = models.CharField(max_length=50, blank=True, null=True)
    contact = models.CharField(max_length=100, blank=True, null=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.PROTECT, blank=True, null=True)
    preservation_plan = models.ForeignKey(PreservationPlan, on_delete=models.PROTECT, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    data_volume = FileSizeField(default=0, blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    embargo_date = models.DateField(blank=True, null=True)
    doi = models.BooleanField(blank=True, verbose_name='DOI', null=True)
    sample_type = models.CharField(max_length=50, blank=True, null=True)
    sample_destination = models.CharField(max_length=100, blank=True, null=True)
    issues = models.TextField(blank=True, null=True)
    data_location = models.CharField(max_length=100, blank=True, null=True)
    responsibility = models.CharField(max_length=50, blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self._meta.object_name} ({self.data_product_type.title()} Data Product) - {self.name if self.name else self.description}'
