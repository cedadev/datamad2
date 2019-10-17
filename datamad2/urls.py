from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.grant_list, name='grant_list'),
    path('grant/<int:pk>/', views.grant_detail, name='grant_detail'),
    path('grant/<int:pk>/claim', views.claim, name='claim'),
    path('accounts/', include('django.contrib.auth.urls',)),
    path('accounts/', views.my_account, name='my_account')
]
