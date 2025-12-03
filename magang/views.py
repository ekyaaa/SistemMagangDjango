from django.shortcuts import render
from .models import Lowongan

# Create your views here.
def home(request):
    """Landing page showing list of available internships"""
    magang_list = Lowongan.objects.select_related('departement').order_by('-tanggal_mulai')
    
    context = {
        'magang_list': magang_list
    }
    return render(request, 'list_magang_screen.html', context)