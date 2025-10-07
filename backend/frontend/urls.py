from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('landlord-login/', views.landlord_login, name='landlord_login'),
    path('tenant-login/', views.tenant_login, name='tenant_login'),
    path('landlord-register/', views.landlord_register, name='landlord_register'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
