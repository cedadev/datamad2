from django.urls import path, include
from dmp import views

urlpatterns = [
    path('project_list', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('dataproduct/new/', views.dataproduct_new, name='dataproduct_new')
]