from django.urls import path, include
from dmp import views

urlpatterns = [
    path('project_list', views.project_list, name='project_list'),
]