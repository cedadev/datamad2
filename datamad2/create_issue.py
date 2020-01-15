from jira import JIRA, JIRAError

# need to change to oauth
# key_cert_data = None
# with open(key_cert, 'r') as key_cert_file:
#     key_cert_data = key_cert_file.read()
#
# oauth_dict = {
#     'access_token': 'foo',
#     'access_token_secret': 'bar',
#     'consumer_key': 'jira-oauth-consumer',
#     'key_cert': key_cert_data
# }
# auth_jira = JIRA(oauth=oauth_dict)


def set_options(user):
    api_token = "KwX9QToAzbAkZ1ByJJmYECA1"
    options = {'server': 'https://jira.ceh.ac.uk/'}
    jira = JIRA(options, basic_auth=(str(user), 'bananabread'))
    return jira


def make_issue(user, imported_grant, grant):
    jira = set_options(user)
    issue_dict = {
        'project': str(user.data_centre),
        'summary': str(imported_grant.grant_ref) + ' : ' + str(imported_grant.title),
        'description': 'Alternative data contact email: ' + str(grant.alt_data_contact_email) +
        '\n Alternative data contact phone number: ' + str(grant.alt_data_contact_phone) +
        '\n Other data centre: ' + str(grant.other_data_centre) +
        '\n Date contacted PI: ' + str(grant.date_contacted_pi) +
        '\n Will the grant produce data? ' + str(grant.will_grant_produce_data) +
        '\n Datasets delivered? ' + str(grant.sanctions_recommended) +
        '\n Case for support found? ' + str(grant.case_for_support_found) +
        '\n Abstract: ' + str(imported_grant.abstract),
        'issuetype': {'name': 'Data Management Tracking'},
        #'customfield_11660': str(imported_grant.actual_start_date), # grant start
        #'customfield_11662': str(imported_grant.grant.date_contacted_pi), # initial contact
        'customfield_11658': str(imported_grant.grant_ref),# NERC reference
        'customfield_11659': str(imported_grant.grant_holder),# PI
        'customfield_11862': str(imported_grant.research_org), # Research organisation
        'customfield_11663': {'value': str(user.data_centre)},  # primary data centre
        #'customfield_11664': [{'value': str(imported_grant.grant.other_data_centre)},]# secondary data centre
    }

    new_issue = jira.create_issue(fields=issue_dict)
    jira.assign_issue(new_issue, str(user))
    return new_issue

# def check_issue_exists(user, summary):
#     jira = set_options(user)
#     try:
#         issue = jira.search_issues(f'summary={summary}')
#         print(issue)
#         return True
#     except JIRAError as err:
#         print('issue not found')
#         return False


def get_link(user, grant_ref):
    jira = set_options(user)
    issues = jira.search_issues(f'summary~{grant_ref}')
    for issue in issues:
        link = issue.permalink()
        return link




