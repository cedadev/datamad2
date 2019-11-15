from django.urls import path, include
from rest_framework import routers
from datamad2_api import views

router = routers.DefaultRouter()
router.register(r'grants', views.GrantViewSet)
router.register(r'importedgrants', views.ImportedGrantViewSet)
router.register(r'users', views.MyUserViewSet)

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]