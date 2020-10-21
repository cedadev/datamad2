from jira import JIRA
from django.conf import settings
from django.urls import reverse
import datetime
from jira.exceptions import JIRAError
from django.contrib import messages

FIELD_MAPPING = {
    'start_date_field': 'str(imported_grant.actual_start_date)',
    'end_date_field': 'str(imported_grant.actual_end_date)',
    'grant_ref_field': 'imported_grant.grant_ref',
    'pi_field': 'imported_grant.grant_holder',
    'research_org_field': 'imported_grant.research_org',
    'primary_datacentre_field': 'request.user.data_centre.name'
}


def get_jira_client(request):
    """
    Returns a provisioned JIRA client
    """
    oauth_dict = {
        'access_token': request.session.get('jira_access_token'),
        'access_token_secret': request.session.get('jira_access_token_secret'),
        'consumer_key': settings.JIRA_CONSUMER_KEY,
        'key_cert': settings.JIRA_PRIVATE_RSA_KEY
    }

    return JIRA(settings.JIRA_SERVER, oauth=oauth_dict)


def make_issue(request, imported_grant):
    """
    Convert a grant into a JIRA ticket
    :param request: Django request object
    :param imported_grant:
    :return: JIRA issue. Either a newly created one or the first result from the search
    """
    jira = get_jira_client(request)
    issue_dict = {
        'project': str(request.user.data_centre.jira_project),
        'summary': f'{imported_grant.grant_ref}:{imported_grant.title}',
        'description': imported_grant.abstract,
        'issuetype': {'id': str(request.user.data_centre.jiraissuetype_set.first().issuetype)},
    }

    for field, value in request.user.data_centre.jira_issue_fields.items():
        mapped_datamad_field = FIELD_MAPPING.get(field)
        if mapped_datamad_field:
            if field == 'primary_datacentre_field':
                issue_dict[value] = {'value': eval(mapped_datamad_field)}
            else:
                issue_dict[value] = eval(mapped_datamad_field)

    # Check if issue already exists
    grant_ref = imported_grant.grant_ref.replace('/', '\\u002f')
    results = jira.search_issues(f'summary~{grant_ref}')

    # Create a new one if none found or return first hit (there should only be one)
    if not results:
        new_issue = jira.create_issue(fields=issue_dict)

        # Generate back-reference to datamad
        datamad_permalink = request.build_absolute_uri(reverse('grant_detail', kwargs={'pk': imported_grant.grant.pk}))

        # Add backreference to datamad
        jira.add_simple_link(new_issue, {
            'url': datamad_permalink,
            'title': f'View grant: {imported_grant.grant_ref} in Datamad'
        })

        # create subtasks
        subtasks = request.user.data_centre.subtask_set.all()
        for task in subtasks:
            create_subtask(task, request, new_issue, imported_grant)

    else:
        new_issue = results[0]

    return new_issue


def create_subtask(subtask, request, new_issue, imported_grant):

    jira = get_jira_client(request)

    if subtask.ref_time == 'end_date':
        ref_time = imported_grant.actual_end_date
    else:
        ref_time = imported_grant.actual_start_date

    subtask_dict = {'project': str(request.user.data_centre.jira_project),
                    'summary': f"{imported_grant.grant_ref}:{subtask.name}",
                    'description': '',
                    'issuetype': {'name': 'Sub-Task'},
                    'parent': {'key': new_issue.key},
                    'customfield_11660': str(imported_grant.actual_start_date), # grant start date
                    'duedate': str(ref_time + datetime.timedelta(weeks=subtask.schedule_time))}

    subtask = jira.create_issue(fields=subtask_dict)
    # jira.assign_issue(subtask, request.user.email)