from rest_framework import serializers
from .models import Unit, Lease, MaintenanceRequest
from accounts.models import User


class UnitSerializer(serializers.ModelSerializer):
    landlord_email = serializers.EmailField(source='landlord.user.email', read_only=True)
    
    class Meta:
        model = Unit
        fields = '__all__'
        read_only_fields = ('landlord', 'created_at', 'updated_at')


class LeaseSerializer(serializers.ModelSerializer):
    tenant_email = serializers.EmailField(source='tenant.email', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    
    class Meta:
        model = Lease
        fields = '__all__'
        read_only_fields = ('created_at',)


class MaintenanceRequestSerializer(serializers.ModelSerializer):
    tenant_email = serializers.EmailField(source='tenant.email', read_only=True)
    unit_name = serializers.CharField(source='unit.name', read_only=True)
    
    class Meta:
        model = MaintenanceRequest
        fields = '__all__'
        read_only_fields = ('tenant', 'created_at', 'updated_at')
