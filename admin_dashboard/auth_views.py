from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def custom_logout(request):
    """Custom logout view that handles both GET and POST"""
    logout(request)
    return redirect('/admin/login/')
