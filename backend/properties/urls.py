from django.urls import path
from . import views

urlpatterns = [
    path('units/', views.UnitListCreateView.as_view(), name='unit_list_create'),
    path('units/<int:pk>/', views.UnitDetailView.as_view(), name='unit_detail'),
    path('leases/', views.LeaseListCreateView.as_view(), name='lease_list_create'),
    path('leases/<int:pk>/', views.LeaseDetailView.as_view(), name='lease_detail'),
    path('maintenance/', views.MaintenanceRequestListCreateView.as_view(), name='maintenance_list_create'),
    path('maintenance/<int:pk>/', views.MaintenanceRequestDetailView.as_view(), name='maintenance_detail'),
]

