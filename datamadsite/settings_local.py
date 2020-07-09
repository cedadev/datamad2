from django.contrib.messages import constants as message_constants
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Redirect to home URL after login (Default redirects to /accounts/profile/)
LOGIN_REDIRECT_URL = '/'
# Redirect to login page after logging out
LOGOUT_REDIRECT_URL = '/accounts/login'

AUTH_USER_MODEL = 'datamad2.User'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MESSAGE_LEVEL = message_constants.DEBUG

JIRA_KEY_PATH = ''
