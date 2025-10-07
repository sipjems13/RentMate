#!/usr/bin/env python
"""
Test script to verify Django setup
"""
import os
import sys
import django

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rentmate.settings')

try:
    django.setup()
    print("✓ Django setup successful!")
    
    # Test imports
    from accounts.models import User
    from properties.models import Unit
    print("✓ Models imported successfully!")
    
    # Test database connection
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT 1")
    print("✓ Database connection successful!")
    
    print("\nDjango backend is ready to use!")
    print("Run 'python manage.py runserver' to start the development server")
    
except Exception as e:
    print(f"✗ Error: {e}")
    sys.exit(1)
