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
    options = {'server': 'https://jira.ceh.ac.uk/'}
    jira = JIRA(options, basic_auth=(str(user), 'bananabread'))
    return jira


def make_issue(user, imported_grant):
    jira = set_options(user)
    issue_dict = {
        'project': 'CEDA',
        'summary': str(imported_grant.grant_ref) + ' : ' + str(imported_grant.title),
        'description': str(imported_grant.abstract),
        'issuetype': {'name': 'Data Management Tracking'},
    }
    new_issue = jira.create_issue(fields=issue_dict)
    jira.assign_issue(new_issue, str(user))
    link = new_issue.permalink()
    return link


def check_issue_exists(user, summary):
    try:
        jira = set_options(user)
        issue = jira.issue(str(summary))
    except JIRAError as err:
        return False




