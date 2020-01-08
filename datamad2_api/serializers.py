from datamad2.models import Grant, ImportedGrant, User
from rest_framework import serializers
from django.contrib.auth.models import Permission

class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant
        fields = '__all__'


class ImportedGrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImportedGrant
        fields = '__all__'
        depth = 1


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

