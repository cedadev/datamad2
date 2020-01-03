from datamad2.models import Grant, ImportedGrant, User
from rest_framework import serializers


class GrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Grant
        fields = '__all__'


class ImportedGrantSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImportedGrant
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    class Meta:
        model = User
        fields = '__all__'

