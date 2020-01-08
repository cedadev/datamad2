from django.urls import path, include, re_path
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

schema_view = get_schema_view(
    openapi.Info(
        title="dataMAD",
        default_version="v1",
    )
)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]