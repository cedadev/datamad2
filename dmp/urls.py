from django.urls import path, include
from dmp import views

urlpatterns = [
    path('projects', views.project_list, name='project_list'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('dataproduct/new/<int:project_id>', views.dataproduct_new, name='dataproduct_new'),
    path('dataproduct/edit/<int:pk>/<int:project_id>', views.dataproduct_edit, name='dataproduct_edit'),
    path('dataproduct/delete/<int:pk>/', views.dataproduct_delete, name='dataproduct_delete'),
    path('dataproduct/<int:pk>/', views.dataproduct_detail, name='dataproduct_detail')
]
