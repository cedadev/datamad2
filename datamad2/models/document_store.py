# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '22 Apr 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.db import models
import hashlib


class Document(models.Model):
    title = models.CharField(max_length=100)
    upload = models.FileField(upload_to='')
    last_modified = models.DateTimeField(auto_now=True)
    grant = models.ForeignKey('Grant', on_delete=models.CASCADE)
    checksum = models.CharField(max_length=100, blank=True)

    def set_title(self):
        """
        Default the title to be the file name if nothing set on upload
        """
        if not self.title:
            self.title = self.upload.name

    def generate_checksum(self):
        """
        Generate an MD5 checksum to check for file changes
        """
        if not self.checksum:
            md5 = hashlib.md5()
            for chunk in self.upload.chunks():
                md5.update(chunk)
            self.checksum = md5.hexdigest()

    def save(self, *args, **kwargs):
        self.set_title()
        self.generate_checksum()
        super().save(*args, **kwargs)


class DMPDocument(Document):
    pass


