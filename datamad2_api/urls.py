from django.urls import path, include
from rest_framework import routers
from datamad2_api import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = routers.DefaultRouter()
router.register(r'grants', views.GrantViewSet)
router.register(r'importedgrants', views.ImportedGrantViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'permission', views.PermissionViewSet)



urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]