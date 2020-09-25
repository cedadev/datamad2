from django.urls import path, include
from datamad2 import views

urlpatterns = [
    path('', views.FacetedGrantListView.as_view(), name='grant_list'),
    path('grant/<int:pk>/', views.grant_detail, name='grant_detail'),
    path('grant/<int:pk>/jira_convert', views.push_to_jira, name='jira_convert'),
    path('grant/<int:pk>/claim', views.claim, name='claim'),
    path('accounts/', include('django.contrib.auth.urls',)),
    path('account/details', views.MyAccountDetailsView.as_view(), name='my_account'),
    path('account/preferences', views.MyAccountPreferencesView.as_view(), name='preferences'),
    path('account/datacentre', (views.MyAccountDatacentreView.as_view()), name='datacentre'),
    path('account/datacentre/new_user', (views.MyAccountNewUserView.as_view()), name='new_user'),
    path('account/datacentre/jira-issue', (views.MyAccountDatacentreIssueTypeView.as_view()), name='issue_type'),
    path('account/datacentre/template', (views.DocumentTemplateListView.as_view()), name='document_template_list'),
    path('account/datacentre/template/<int:pk>', (views.DocumentTemplateUpdateView.as_view()), name='document_template_update'),
    path('account/datacentre/template/new', (views.DocumentTemplateCreateView.as_view()), name='document_template_create'),
    path('grant/<int:pk>/change_claim/', views.change_claim, name='change_claim'),
    path('grant/<int:pk>/unclaim', views.unclaim, name='unclaim'),
    path('grant/<int:pk>/history/', views.grant_history, name='grant_history'),
    path('grant/<int:pk>/history/<int:imported_pk>', views.grant_history_detail, name='grant_history_detail'),
    path('grant/<int:pk>/edit/', views.grantinfo_edit, name='grantinfo_edit'),
    path('grant/<int:pk>/dataproducts', views.DataProductView.as_view(), name='dataproduct_view'),
    path('document/upload/<int:pk>', views.document_upload, name='document_upload'),
    path('document/<int:pk>/delete/', views.delete_file, name='delete_file'),
    path('document/multiple_upload/', views.multiple_document_upload, name='multi_document_upload'),
]