from django.urls import path
from . import views

urlpatterns = [
    path('', views.grant_list, name='grant_list'),
    path('grant/<int:pk>/', views.grant_detail, name='grant_detail'),
    path('grant/<int:pk>/claim', views.claim, name="claim")
]