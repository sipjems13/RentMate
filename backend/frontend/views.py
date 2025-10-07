from django.shortcuts import render


def index(request):
    """Home page"""
    return render(request, 'index.html')


def landlord_login(request):
    """Landlord login page"""
    return render(request, 'landlord-login.html')


def tenant_login(request):
    """Tenant login page"""
    return render(request, 'tenant-login.html')


def landlord_register(request):
    """Landlord registration page"""
    return render(request, 'landlord-register.html')


def dashboard(request):
    """Dashboard page"""
    return render(request, 'dashboard.html')
