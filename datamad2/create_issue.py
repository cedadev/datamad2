from jira import JIRA
from django.conf import settings


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
        'issuetype': {'name': 'Data Management Tracking'},
        #'customfield_11660': str(imported_grant.actual_start_date), # grant start
        #'customfield_11662': str(imported_grant.grant.date_contacted_pi), # initial contact
        'customfield_11658': imported_grant.grant_ref,# NERC reference
        'customfield_11659': imported_grant.grant_holder,# PI
        'customfield_11862': imported_grant.research_org, # Research organisation
        'customfield_11663': {'value': request.user.data_centre.name},  # primary data centre
        #'customfield_11664': [{'value': str(imported_grant.grant.other_data_centre)},]# secondary data centre
    }

    # Check if issue already exists
    grant_ref = imported_grant.grant_ref.replace('/', '\\u002f')
    results = jira.search_issues(f'summary~{grant_ref}')

    # Create a new one if none found or return first hit (there should only be one)
    if not results:
        new_issue = jira.create_issue(fields=issue_dict)

        # Assign issue to the creator
        jira.assign_issue(new_issue, request.user.email)
    else:
        new_issue = results[0]

    return new_issue


