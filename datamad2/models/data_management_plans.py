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


def file_name(instance, filename):
    h = instance.checksum
    datacentre = instance.datacentre.name
    basename, ext = os.path.splitext(filename)
    return os.path.join('document_templates', datacentre, f'{h}{ext}')


class DocumentTemplate(models.Model):
    datacentre = models.ForeignKey(DataCentre, on_delete=models.CASCADE)
    template = models.FileField(upload_to=file_name, storage=MediaFileSystemStorage())
    name = models.CharField(max_length=100, blank=True, help_text='Name will default to mach uploaded file')
    description = models.TextField(blank=True, help_text="Short description to help other users understand what the template is used for")

    def _generate_checksum(self):
        """
        Generate an MD5 checksum to check for file changes
        """
        if not self.pk:
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


class DataFormat(models.Model):
    format = models.CharField(max_length=50)


class PreservationPlan(models.Model):
    short_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True)


class DataProduct(models.Model):
    CHOICES = (
        ('digital', 'Digital Dataset'),
        ('model', 'Model Source Code'),
        ('physical', 'Pysical Collections & Samples'),
        ('hardcopy', 'Hardcopy Records'),
        ('third_party', 'Third Party/Existing Datasets'),
    )
    grant = models.ForeignKey(Grant, on_delete=models.CASCADE)
    added = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=100, blank=True)
    data_format = models.ForeignKey(DataFormat, on_delete=models.PROTECT, blank=True)
    preservation_plan = models.ForeignKey(PreservationPlan, on_delete=models.PROTECT, blank=True)
    description = models.TextField(blank=True)
    data_volume = FileSizeField(default=0, blank=True)
    delivery_date = models.DateField(blank=True)
    embargo_date = models.DateField(blank=True)
    doi = models.BooleanField(blank=True, verbose_name='DOI')
    sample_type = models.CharField(max_length=50, blank=True)
    sample_destination = models.CharField(max_length=100, blank=True)
    issues = models.TextField(blank=True)
    data_location = models.CharField(max_length=100, blank=True)
    responsibility = models.CharField(max_length=50, blank=True)
    additional_comments = models.TextField(blank=True)
