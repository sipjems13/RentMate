from django.contrib import admin
from .models import Unit, Lease, MaintenanceRequest


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'landlord', 'city', 'state', 'rent_amount', 'is_available', 'created_at')
    list_filter = ('is_available', 'city', 'state', 'created_at')
    search_fields = ('name', 'address', 'city', 'state')
    list_editable = ('is_available',)


@admin.register(Lease)
class LeaseAdmin(admin.ModelAdmin):
    list_display = ('unit', 'tenant', 'start_date', 'end_date', 'monthly_rent', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date', 'end_date', 'created_at')
    search_fields = ('unit__name', 'tenant__email', 'tenant__first_name', 'tenant__last_name')
    list_editable = ('is_active',)


@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'tenant', 'priority', 'status', 'created_at')
    list_filter = ('priority', 'status', 'created_at')
    search_fields = ('title', 'unit__name', 'tenant__email')
    list_editable = ('status', 'priority')

