from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path

# Register your models here.

# Customize admin site
class CustomAdminSite(admin.AdminSite):
    def index(self, request, extra_context=None):
        # Redirect admin index to dashboard
        return redirect('/dashboard/')

# Override default admin site
admin.site.__class__ = CustomAdminSite
