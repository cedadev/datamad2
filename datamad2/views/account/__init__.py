# encoding: utf-8
"""
Package of views relating to user account and related. This includes User Account Management
as well as Datacentre specific account management e.g. JIRA Issue mappings and
document templates for automatic document templating.
"""
__author__ = 'Richard Smith'
__date__ = '11 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from .datacentre import *
from .user import MyAccountDetailsView, MyAccountPreferencesView, \
    MyAccountUsersView, MyAccountNewUserView, MyAccountEditUserView, \
    MyAccountRemoveUserView