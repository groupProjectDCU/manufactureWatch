from rest_framework import serializers
from machinery.models import Machinery

# serializers for api requests
# TODO: machinery collection serializer and machinery assignment serializer

# machinery serializer
class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ['machine_id', 'name', 'model', 'description', 'status', 'priority']

