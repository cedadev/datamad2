from datamad2.models import Grant, ImportedGrant, User
from rest_framework import viewsets
from datamad2_api.serializers import GrantSerializer, ImportedGrantSerializer, UserSerializer


class GrantViewSet(viewsets.ModelViewSet):
    # everything in triple quotes is seen by the user
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = Grant.objects.all()
    serializer_class = GrantSerializer


class ImportedGrantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = ImportedGrant.objects.all()
    serializer_class = ImportedGrantSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows grants to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
