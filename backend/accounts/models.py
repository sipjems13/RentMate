from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with role-based authentication"""
    
    ROLE_CHOICES = [
        ('landlord', 'Landlord'),
        ('tenant', 'Tenant'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class Landlord(models.Model):
    """Landlord profile extending User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='landlord_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Landlord: {self.user.email}"


class Tenant(models.Model):
    """Tenant profile extending User"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tenant_profile')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Tenant: {self.user.email}"
