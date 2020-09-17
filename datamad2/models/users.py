# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '22 Apr 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


class DataCentre(models.Model):
    CHOICES = (
        ('BODC', 'BODC'),
        ('CEDA', 'CEDA'),
        ('EIDC', 'EIDC'),
        ('NGDC', 'NGDC'),
        ('PDC', 'PDC'),
        ('ADS', 'ADS')
    )

    name = models.CharField(max_length=100, null=True, unique=True, choices=CHOICES, verbose_name='Datacentre Name')
    jira_project = models.CharField(max_length=100, blank=True, verbose_name='Data Management JIRA Project')

    # Data Centre Specific JIRA Data Management Tracking JIRA issue details
    issuetype = models.IntegerField(help_text='JIRA Data Management issue type ID', blank=True, null=True)
    start_date_field = models.CharField(max_length=100, blank=True, verbose_name='Start Date Field ID')
    end_date_field = models.CharField(max_length=100, blank=True, verbose_name='End Date Field ID')
    grant_ref_field = models.CharField(max_length=100, blank=True, verbose_name='Grant Ref Field ID')
    pi_field = models.CharField(max_length=100, verbose_name='Principle Investigator Field ID', blank=True)
    research_org_field = models.CharField(max_length=100, verbose_name='Research Org Field ID', blank=True)
    primary_datacentre_field = models.CharField(max_length=100, blank=True, verbose_name='Primary Datacentre Field ID')

    def __str__(self):
        return f"{self.name}"

    @property
    def jira_issue_fields(self):

        issue_fields = {k:v for k,v in self.__dict__.items() if k.endswith('field') and v}
        return issue_fields


class Subtask(models.Model):
    data_centre = models.ForeignKey(to=DataCentre, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    schedule_time = models.IntegerField(blank=True, null=True,
                                        help_text='Time in weeks to at which to schedule sub-task in reference to the reference time. '
                                                  'Using a negative value schedules the task before the reference time',
                                        verbose_name='Schedule at')  # in weeks
    ref_time = models.CharField(max_length=200, blank=True, null=True,
                                choices=(("start_date", "Start Date"), ("end_date", "End Date")), help_text=
                                'Start date means the sub-task will be scheduled in reference to the start date. End date means it will be scheduled in reference to the end date.',
                                verbose_name='Reference time')

    def __str__(self):
        return f"{self.name}"


class UserManager(BaseUserManager):
    def _create_user(self, email, password, data_centre=None, **extra_fields):
        """
        Creates and saves a user with given email and password
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email), **extra_fields)

        # Set the username to match the email
        user.username = self.normalize_email(email)
        user.set_password(password)
        user.data_centre = DataCentre.objects.get(name=data_centre)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, datacentre=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, datacentre, **extra_fields)

    def create_superuser(self, email, password=None, datacentre=None, **extra_fields):

        DataCentre.objects.get_or_create(name=None)

        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self._create_user(email, password, datacentre, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.EmailField(max_length=255)
    data_centre = models.ForeignKey('DataCentre', on_delete=models.SET_NULL, null=True, blank=True, to_field='name')
    prefered_facets = models.TextField(null=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    @property
    def preferences(self):
        prefered_facets = []

        if self.prefered_facets:
            prefered_facets = self.prefered_facets.split(',')

        return {
            'prefered_facets': prefered_facets
        }
