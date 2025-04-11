from rest_framework import serializers
from machinery.models import Machinery

# serializers for api requests
# TODO: machinery collection serializer and machinery assignment serializer

# Basic machinery serializer for list views
class MachinerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ['machine_id', 'name', 'model', 'description', 'status', 'priority']

# Detailed machinery serializer for detail views and manager operations
class MachineryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machinery
        fields = ['machine_id', 'name', 'model', 'description', 'status', 'priority', 
                 'maintenance_history', 'last_maintained', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

