from datamad2.models import Grant, ImportedGrant, User
from rest_framework import viewsets
from datamad2_api.serializers import GrantSerializer, ImportedGrantSerializer, UserSerializer, PermissionSerializer
from django.contrib.auth.models import Permission

class GrantViewSet(viewsets.ModelViewSet):
    # everything in triple quotes is seen by the user
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer
    filterset_fields = ['assigned_data_centre', 'grant_ref']


class ImportedGrantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = ImportedGrant.objects.all()
    serializer_class = ImportedGrantSerializer
    filterset_fields = ['title', 'grant_ref']

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filterset_fields = ['email']

class PermissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows permissions to be viewed or edited.
    """
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
