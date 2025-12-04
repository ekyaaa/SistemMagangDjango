from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Lowongan, Pendaftar, TransaksiPendaftaran
import json

# Create your views here.
def home(request):
    search_query = request.GET.get('search', '').strip()
    
    context = {
        'search_query': search_query
    }
    return render(request, 'list_magang_screen.html', context)


def get_lowongan_api(request):
    """API endpoint untuk mengambil list lowongan via AJAX"""
    search_query = request.GET.get('search', '').strip()
    
    magang_list = Lowongan.objects.select_related('departement').order_by('-tanggal_mulai')
    
    if search_query:
        magang_list = magang_list.filter(
            Q(posisi__icontains=search_query) | 
            Q(departement__nama_dept__icontains=search_query)
        )
    
    # Convert queryset to list of dicts for JSON response
    data = [
        {
            'id_lowongan': lowongan.id_lowongan,
            'posisi': lowongan.posisi,
            'nama_dept': lowongan.departement.nama_dept,
            'deskripsi': lowongan.deskripsi,
            'tanggal_mulai': lowongan.tanggal_mulai.strftime('%Y-%m-%d'),
            'tanggal_selesai': lowongan.tanggal_selesai.strftime('%Y-%m-%d'),
        }
        for lowongan in magang_list
    ]
    
    return JsonResponse({
        'success': True,
        'data': data,
        'total': len(data)
    })


@csrf_exempt
def submit_pendaftaran(request):
    """API endpoint untuk submit pendaftaran magang via AJAX"""
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Method not allowed'
        }, status=405)
    
    try:
        # Get form data
        id_lowongan = request.POST.get('lowongan')
        nik = request.POST.get('nik')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        no_telp = request.POST.get('no_telp')
        university = request.POST.get('university')
        major = request.POST.get('major')
        ipk = request.POST.get('ipk')
        cv_file = request.FILES.get('path_cv')
        
        # Validate required fields
        if not all([id_lowongan, nik, name, gender, dob, address, no_telp, university, major, cv_file]):
            return JsonResponse({
                'success': False,
                'message': 'Semua field wajib diisi'
            }, status=400)
        
        # Check if lowongan exists
        try:
            lowongan = Lowongan.objects.get(id_lowongan=id_lowongan)
        except Lowongan.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Lowongan tidak ditemukan'
            }, status=404)
        
        # Check if NIK already exists
        if Pendaftar.objects.filter(nik=nik).exists():
            return JsonResponse({
                'success': False,
                'message': 'NIK sudah terdaftar. Gunakan NIK yang berbeda.'
            }, status=400)
        
        # Validate file type
        if not cv_file.name.endswith('.pdf'):
            return JsonResponse({
                'success': False,
                'message': 'File CV harus berformat PDF'
            }, status=400)
        
        # Validate file size (max 2MB)
        if cv_file.size > 2 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'message': 'Ukuran file CV maksimal 2MB'
            }, status=400)
        
        # Create Pendaftar
        pendaftar = Pendaftar.objects.create(
            lowongan=lowongan,
            nik=nik,
            name=name,
            gender=gender,
            dob=dob,
            address=address,
            no_telp=no_telp,
            university=university,
            major=major,
            path_cv=cv_file,
            ipk=ipk if ipk else None
        )
        
        # Create TransaksiPendaftaran
        transaksi = TransaksiPendaftaran.objects.create(
            pendaftar=pendaftar,
            lowongan=lowongan,
            status='pending'
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Pendaftaran berhasil! Data Anda sedang dalam proses review.',
            'data': {
                'id_pendaftar': pendaftar.id_pendaftar,
                'id_transaksi': transaksi.id_transaksi_pendaftaran,
                'status': transaksi.status
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }, status=500)