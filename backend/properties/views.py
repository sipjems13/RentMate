from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Unit, Lease, MaintenanceRequest
from .serializers import UnitSerializer, LeaseSerializer, MaintenanceRequestSerializer
from accounts.models import Landlord


class UnitListCreateView(generics.ListCreateAPIView):
    """List and create units"""
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return Unit.objects.filter(landlord__user=self.request.user)
        return Unit.objects.filter(is_available=True)
    
    def perform_create(self, serializer):
        if self.request.user.role != 'landlord':
            raise permissions.PermissionDenied("Only landlords can create units")
        landlord = get_object_or_404(Landlord, user=self.request.user)
        serializer.save(landlord=landlord)


class UnitDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a unit"""
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return Unit.objects.filter(landlord__user=self.request.user)
        return Unit.objects.all()


class LeaseListCreateView(generics.ListCreateAPIView):
    """List and create leases"""
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return Lease.objects.filter(unit__landlord__user=self.request.user)
        return Lease.objects.filter(tenant=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.role != 'landlord':
            raise permissions.PermissionDenied("Only landlords can create leases")
        serializer.save()


class LeaseDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a lease"""
    serializer_class = LeaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return Lease.objects.filter(unit__landlord__user=self.request.user)
        return Lease.objects.filter(tenant=self.request.user)


class MaintenanceRequestListCreateView(generics.ListCreateAPIView):
    """List and create maintenance requests"""
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return MaintenanceRequest.objects.filter(unit__landlord__user=self.request.user)
        return MaintenanceRequest.objects.filter(tenant=self.request.user)
    
    def perform_create(self, serializer):
        if self.request.user.role != 'tenant':
            raise permissions.PermissionDenied("Only tenants can create maintenance requests")
        serializer.save(tenant=self.request.user)


class MaintenanceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a maintenance request"""
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.role == 'landlord':
            return MaintenanceRequest.objects.filter(unit__landlord__user=self.request.user)
        return MaintenanceRequest.objects.filter(tenant=self.request.user)

