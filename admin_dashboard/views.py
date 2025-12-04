from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required, user_passes_test
from .service import DashboardService

# Create your views here.

def is_admin(user):
    """Check if user is admin/staff"""
    return user.is_staff or user.is_superuser

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
def dashboard(request):
    """Render halaman dashboard admin"""
    return render(request, 'dashboard.html')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
def manajemen_lowongan(request):
    """Render halaman manajemen lowongan dan departemen"""
    return render(request, 'manajemen_lowongan.html')

@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
def manajemen_pendaftar(request):
    """Render halaman manajemen pendaftar"""
    return render(request, 'manajemen_pendaftar.html')


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def get_dashboard_stats(request):
    """API endpoint untuk mendapatkan statistik dashboard"""
    if request.method == 'GET':
        try:
            stats = DashboardService.get_statistics()
            return JsonResponse({
                'success': True,
                'data': stats
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def get_trend_chart_data(request):
    """API endpoint untuk data chart tren pendaftaran"""
    if request.method == 'GET':
        try:
            days = request.GET.get('days', 30)
            trend_data = DashboardService.get_trend_data(int(days))
            return JsonResponse({
                'success': True,
                'data': trend_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def get_department_chart_data(request):
    """API endpoint untuk data chart distribusi departemen"""
    if request.method == 'GET':
        try:
            dept_data = DashboardService.get_department_distribution()
            return JsonResponse({
                'success': True,
                'data': dept_data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def get_recent_applicants(request):
    """API endpoint untuk mendapatkan daftar pendaftar terbaru"""
    if request.method == 'GET':
        try:
            limit = request.GET.get('limit', 10)
            applicants = DashboardService.get_recent_applicants(int(limit))
            return JsonResponse({
                'success': True,
                'data': applicants
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


# === CRUD LOWONGAN ===
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_lowongan_list(request):
    """API untuk mendapatkan list lowongan"""
    if request.method == 'GET':
        try:
            search = request.GET.get('search', '')
            lowongan_list = DashboardService.get_all_lowongan(search)
            return JsonResponse({
                'success': True,
                'data': lowongan_list
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_lowongan_create(request):
    """API untuk membuat lowongan baru"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            lowongan = DashboardService.create_lowongan(data)
            return JsonResponse({
                'success': True,
                'message': 'Lowongan berhasil ditambahkan',
                'data': {'id': lowongan.id_lowongan}
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_lowongan_detail(request, id_lowongan):
    """API untuk mendapatkan detail lowongan"""
    if request.method == 'GET':
        try:
            lowongan = DashboardService.get_lowongan_by_id(id_lowongan)
            return JsonResponse({
                'success': True,
                'data': lowongan
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=404)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_lowongan_update(request, id_lowongan):
    """API untuk update lowongan"""
    if request.method == 'PUT':
        try:
            import json
            data = json.loads(request.body)
            lowongan = DashboardService.update_lowongan(id_lowongan, data)
            return JsonResponse({
                'success': True,
                'message': 'Lowongan berhasil diupdate'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_lowongan_delete(request, id_lowongan):
    """API untuk hapus lowongan"""
    if request.method == 'DELETE':
        try:
            DashboardService.delete_lowongan(id_lowongan)
            return JsonResponse({
                'success': True,
                'message': 'Lowongan berhasil dihapus'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


# === CRUD DEPARTEMEN ===
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_departemen_list(request):
    """API untuk mendapatkan list departemen"""
    if request.method == 'GET':
        try:
            search = request.GET.get('search', '')
            dept_list = DashboardService.get_all_departemen(search)
            return JsonResponse({
                'success': True,
                'data': dept_list
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_departemen_create(request):
    """API untuk membuat departemen baru"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            dept = DashboardService.create_departemen(data)
            return JsonResponse({
                'success': True,
                'message': 'Departemen berhasil ditambahkan',
                'data': {'id': dept.id_dept}
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_departemen_detail(request, id_dept):
    """API untuk mendapatkan detail departemen"""
    if request.method == 'GET':
        try:
            dept = DashboardService.get_departemen_by_id(id_dept)
            return JsonResponse({
                'success': True,
                'data': dept
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=404)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_departemen_update(request, id_dept):
    """API untuk update departemen"""
    if request.method == 'PUT':
        try:
            import json
            data = json.loads(request.body)
            dept = DashboardService.update_departemen(id_dept, data)
            return JsonResponse({
                'success': True,
                'message': 'Departemen berhasil diupdate'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_departemen_delete(request, id_dept):
    """API untuk hapus departemen"""
    if request.method == 'DELETE':
        try:
            DashboardService.delete_departemen(id_dept)
            return JsonResponse({
                'success': True,
                'message': 'Departemen berhasil dihapus'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


# === PENDAFTAR VIEWS ===
@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_pendaftar_pending(request):
    """API untuk mendapatkan daftar pendaftar pending"""
    if request.method == 'GET':
        try:
            search = request.GET.get('search', '')
            data = DashboardService.get_pending_applicants(search)
            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_pendaftar_history(request):
    """API untuk mendapatkan riwayat pendaftar"""
    if request.method == 'GET':
        try:
            search = request.GET.get('search', '')
            status_filter = request.GET.get('status', '')
            data = DashboardService.get_applicants_history(search, status_filter)
            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_pendaftar_detail(request, id_transaksi):
    """API untuk mendapatkan detail pendaftar"""
    if request.method == 'GET':
        try:
            data = DashboardService.get_applicant_detail(id_transaksi)
            return JsonResponse({
                'success': True,
                'data': data
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)


@login_required(login_url='/admin/login/')
@user_passes_test(is_admin, login_url='/admin/login/')
@csrf_exempt
def api_pendaftar_update_status(request, id_transaksi):
    """API untuk update status pendaftar"""
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            status = data.get('status')
            
            if not status or status not in ['approved', 'rejected']:
                return JsonResponse({
                    'success': False,
                    'message': 'Status tidak valid'
                }, status=400)
            
            DashboardService.update_applicant_status(id_transaksi, status)
            
            message = 'Kandidat berhasil diterima' if status == 'approved' else 'Kandidat berhasil ditolak'
            
            return JsonResponse({
                'success': True,
                'message': message
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=500)
