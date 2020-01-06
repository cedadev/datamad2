from django.urls import path, include
from rest_framework import routers
from datamad2_api import views
from rest_framework.schemas import get_schema_view

router = routers.DefaultRouter()
router.register(r'grants', views.GrantViewSet)
router.register(r'importedgrants', views.ImportedGrantViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'permission', views.PermissionViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('openapi', get_schema_view(
        title="DataMAD",
        url='http://127.0.0.1:8000',
        urlconf='datamad2_api.urls',
        description="API for dataMAD",
        version="1.0.0"
    ), name='openapi-schema')
]