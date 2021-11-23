# encoding: utf-8
"""
Views relating to creating JIRA tickets
"""
__author__ = 'Richard Smith'
__date__ = '10 Dec 2020'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

# Datamad imports
from datamad2.models import Grant, JIRATicket
from datamad2.utils import rgetattr
from datamad2.create_issue import make_issue
import datamad2.forms as datamad_forms
from .mixins import DatacentreAdminTestMixin
from .generic import ObjectDeleteView
from django.views.generic.edit import UpdateView

# Django imports
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.html import mark_safe
from django.urls import reverse

# Utility imports
from jira_oauth.decorators import jira_access_token_required
from jira.exceptions import JIRAError

# Python imports
import logging


logger = logging.getLogger(__name__)


@login_required
@jira_access_token_required
def push_to_jira(request, pk):
    """
    Create a JIRA ticket from a grant.
    Once the ticket is created, save a link to the ticket with the grant for easy retrieval
    :param request:
    :param pk:
    :return:
    """
    grant = get_object_or_404(Grant, pk=pk)
    jira_required_fields = [('jiraissuetype.issuetype','issue_type' ), ('jira_project','datacentre')]

    # Make sure the user has a data centre
    if not request.user.data_centre:
        messages.error(request,
                       f'Your account is not attributed to a Datacentre. You need to '
                       f'have a Datacentre before you can perform this action')
        return redirect('grant_detail', pk=pk)

    # Make sure the user's datacentre doesn't already have a JIRA ticket created
    try:
        user_jira_ticket = grant.jiraticket_set.get(datacentre=request.user.data_centre)
    except ObjectDoesNotExist:
        pass
    else:
        if user_jira_ticket:
            messages.warning(request,
                             mark_safe(
                                 'Your datacentre already has a JIRA ticket associated. '
                                 f'<a href="{user_jira_ticket.url}" target="_blank">{user_jira_ticket.datacentre}</a> '
                                 'If the ticket has been removed from JIRA, '
                                 'ask an admin remove the link in DataMAD and try again.'
                             ))
            return redirect('grant_detail', pk=pk)

    # Check for required fields in users datacentre
    for field, view in jira_required_fields:
        if not rgetattr(request.user.data_centre, field, None):
            messages.error(request,
                           mark_safe(
                                f'Not all the required fields have been populated. '
                                f'Populate <i>{field}</i> to allow this operation. '
                                f'Please update field <a href="{reverse(view)}" target="_blank">Here</a>'
                           ))
            return redirect('grant_detail', pk=pk)

    try:
        issue = make_issue(request, grant.importedgrant)
        link = issue.permalink()

        # Save the ticket link to the correct grant
        if link:
            jira_ticket = JIRATicket(
                grant=grant,
                url=link,
                datacentre=request.user.data_centre
            )
            jira_ticket.save()

    except JIRAError as e:
        messages.error(request,
                       f'There was an error when trying to create the JIRA issue. {e.text}')
        logger.error(e, exc_info=True)

    return redirect('grant_detail', pk=pk)


class JIRATicketDeleteView(DatacentreAdminTestMixin, ObjectDeleteView):
    """
    Unlink the JIRA ticket URL from the grant
    """
    model = JIRATicket
    pk_url_kwarg = 'jt_pk'

    def get_success_url(self):
        return reverse('grant_detail', kwargs={'pk': self.kwargs['pk']})


class JIRATicketEditView(DatacentreAdminTestMixin, UpdateView):
    """
    View which presents a form to edit the JIRA link
    """
    model = JIRATicket
    form_class = datamad_forms.UpdateJIRAForm
    pk_url_kwarg = 'jt_pk'
    template_name = 'datamad2/jira_edit.html'

    def get_initial(self):
        initial = super().get_initial()
        initial['url'] = get_object_or_404(JIRATicket, pk=self.kwargs['jt_pk']).url
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['grant'] = get_object_or_404(Grant, pk=self.kwargs['pk'])
        return context

    def get_success_url(self):
        return reverse('grant_detail', kwargs={'pk': self.kwargs['pk']})
