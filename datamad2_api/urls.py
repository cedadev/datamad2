from django.urls import path, include
from rest_framework import routers
from datamad2_api import views
from rest_framework.schemas import get_schema_view
#from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


router = routers.DefaultRouter()
router.register(r'grants', views.GrantViewSet)
router.register(r'importedgrants', views.ImportedGrantViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'permission', views.PermissionViewSet)

schema_view = get_schema_view(title='DataMAD API') #, renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
    path('', schema_view),
]