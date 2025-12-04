from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta, datetime
from magang.models import Pendaftar, Lowongan, TransaksiPendaftaran, Departement


class DashboardService:
    """Service untuk menyediakan data dashboard admin"""
    
    @staticmethod
    def get_statistics():
        """Mendapatkan statistik keseluruhan untuk cards"""
        total_pendaftar = Pendaftar.objects.count()
        
        # Lowongan aktif (tanggal selesai >= hari ini)
        today = timezone.now().date()
        lowongan_aktif = Lowongan.objects.filter(tanggal_selesai__gte=today).count()
        
        # Departemen yang sedang membuka lowongan
        dept_aktif = Lowongan.objects.filter(
            tanggal_selesai__gte=today
        ).values('departement').distinct().count()
        
        # Menunggu review (status pending)
        menunggu_review = TransaksiPendaftaran.objects.filter(status='pending').count()
        
        # Total diterima dan tingkat penerimaan
        total_approved = TransaksiPendaftaran.objects.filter(status='approved').count()
        total_transaksi = TransaksiPendaftaran.objects.count()
        tingkat_penerimaan = round((total_approved / total_transaksi * 100), 0) if total_transaksi > 0 else 0
        
        # Hitung perubahan dari bulan lalu
        last_month = today - timedelta(days=30)
        pendaftar_bulan_ini = Pendaftar.objects.filter(created_at__gte=last_month).count()
        pendaftar_bulan_lalu = total_pendaftar - pendaftar_bulan_ini
        persentase_perubahan = round((pendaftar_bulan_ini / pendaftar_bulan_lalu * 100) - 100, 0) if pendaftar_bulan_lalu > 0 else 0
        
        return {
            'total_pendaftar': total_pendaftar,
            'persentase_perubahan': persentase_perubahan,
            'lowongan_aktif': lowongan_aktif,
            'dept_aktif': dept_aktif,
            'menunggu_review': menunggu_review,
            'tingkat_penerimaan': int(tingkat_penerimaan),
            'total_approved': total_approved
        }
    
    @staticmethod
    def get_trend_data(days=30):
        """Mendapatkan data tren pendaftaran untuk line chart"""
        now = timezone.now()
        today = now.date()
        
        # Ambil data 30 hari terakhir, kelompokkan per 4 hari (8 titik data)
        intervals = []
        data_points = []
        
        for i in range(7, -1, -1):  # 8 titik data, dari yang terlama ke terbaru
            # Hitung rentang waktu untuk setiap interval
            days_back_end = i * 4
            days_back_start = (i + 1) * 4
            
            end_date = today - timedelta(days=days_back_end)
            start_date = today - timedelta(days=days_back_start)
            
            # Query dengan datetime agar mencakup hari ini juga
            if i == 0:  # Interval terakhir sampai sekarang
                count = Pendaftar.objects.filter(
                    created_at__gte=timezone.make_aware(
                        timezone.datetime.combine(start_date, timezone.datetime.min.time())
                    ),
                    created_at__lte=now
                ).count()
            else:
                count = Pendaftar.objects.filter(
                    created_at__gte=timezone.make_aware(
                        timezone.datetime.combine(start_date, timezone.datetime.min.time())
                    ),
                    created_at__lt=timezone.make_aware(
                        timezone.datetime.combine(end_date, timezone.datetime.min.time())
                    )
                ).count()
            
            # Format label tanggal
            label = end_date.strftime('%d %b')
            intervals.append(label)
            data_points.append(count)
        
        return {
            'labels': intervals,
            'data': data_points
        }
    
    @staticmethod
    def get_department_distribution():
        """Mendapatkan distribusi pendaftar per departemen untuk doughnut chart"""
        # Hitung jumlah pendaftar per departemen
        dept_data = TransaksiPendaftaran.objects.values(
            'lowongan__departement__nama_dept'
        ).annotate(
            count=Count('id_transaksi_pendaftaran')
        ).order_by('-count')[:5]  # Top 5 departemen
        
        labels = []
        data = []
        
        for item in dept_data:
            dept_name = item['lowongan__departement__nama_dept']
            # Singkat nama departemen jika terlalu panjang
            if dept_name:
                labels.append(dept_name)
                data.append(item['count'])
        
        return {
            'labels': labels,
            'data': data
        }
    
    @staticmethod
    def get_recent_applicants(limit=10):
        """Mendapatkan daftar pendaftar terbaru dengan berbagai status"""
        recent = TransaksiPendaftaran.objects.select_related(
            'pendaftar', 
            'lowongan',
            'lowongan__departement'
        ).order_by('-created_at')[:limit]
        
        applicants = []
        for transaksi in recent:
            # Buat inisial dari nama
            name_parts = transaksi.pendaftar.name.split()
            initials = ''.join([part[0].upper() for part in name_parts[:2]])
            
            applicants.append({
                'id_transaksi': transaksi.id_transaksi_pendaftaran,
                'name': transaksi.pendaftar.name,
                'initials': initials,
                'position': transaksi.lowongan.posisi,
                'university': transaksi.pendaftar.university,
                'date': transaksi.created_at.strftime('%d %b %Y'),
                'status': transaksi.status,
                'nik': transaksi.pendaftar.nik
            })
        
        return applicants
    
    @staticmethod
    def get_all_lowongan(search=''):
        """Mendapatkan semua lowongan dengan filter search"""
        lowongan_list = Lowongan.objects.select_related('departement').all()
        
        if search:
            lowongan_list = lowongan_list.filter(
                Q(posisi__icontains=search) | 
                Q(departement__nama_dept__icontains=search)
            )
        
        lowongan_list = lowongan_list.order_by('-tanggal_mulai')
        
        result = []
        today = timezone.now().date()
        
        for lowongan in lowongan_list:
            # Tentukan status
            if lowongan.tanggal_selesai >= today:
                status = 'Aktif'
                status_class = 'active'
            else:
                status = 'Selesai'
                status_class = 'completed'
            
            result.append({
                'id': lowongan.id_lowongan,
                'posisi': lowongan.posisi,
                'deskripsi': lowongan.deskripsi,
                'departemen': lowongan.departement.nama_dept,
                'departemen_id': lowongan.departement.id_dept,
                'tanggal_mulai': lowongan.tanggal_mulai.strftime('%Y-%m-%d'),
                'tanggal_selesai': lowongan.tanggal_selesai.strftime('%Y-%m-%d'),
                'periode': f"{lowongan.tanggal_mulai.strftime('%d %b %y')} - {lowongan.tanggal_selesai.strftime('%d %b %y')}",
                'status': status,
                'status_class': status_class
            })
        
        return result
    
    @staticmethod
    def create_lowongan(data):
        """Membuat lowongan baru"""
        lowongan = Lowongan.objects.create(
            posisi=data['posisi'],
            deskripsi=data.get('deskripsi', ''),
            tanggal_mulai=data['tanggal_mulai'],
            tanggal_selesai=data['tanggal_selesai'],
            departement_id=data['departemen_id']
        )
        return lowongan
    
    @staticmethod
    def update_lowongan(id_lowongan, data):
        """Update lowongan yang ada"""
        lowongan = Lowongan.objects.get(id_lowongan=id_lowongan)
        lowongan.posisi = data['posisi']
        lowongan.deskripsi = data.get('deskripsi', '')
        lowongan.tanggal_mulai = data['tanggal_mulai']
        lowongan.tanggal_selesai = data['tanggal_selesai']
        lowongan.departement_id = data['departemen_id']
        lowongan.save()
        return lowongan
    
    @staticmethod
    def delete_lowongan(id_lowongan):
        """Hapus lowongan"""
        lowongan = Lowongan.objects.get(id_lowongan=id_lowongan)
        lowongan.delete()
        return True
    
    @staticmethod
    def get_lowongan_by_id(id_lowongan):
        """Mendapatkan detail lowongan berdasarkan ID"""
        lowongan = Lowongan.objects.select_related('departement').get(id_lowongan=id_lowongan)
        return {
            'id': lowongan.id_lowongan,
            'posisi': lowongan.posisi,
            'deskripsi': lowongan.deskripsi,
            'departemen_id': lowongan.departement.id_dept,
            'tanggal_mulai': lowongan.tanggal_mulai.strftime('%Y-%m-%d'),
            'tanggal_selesai': lowongan.tanggal_selesai.strftime('%Y-%m-%d'),
        }
    
    @staticmethod
    def get_all_departemen(search=''):
        """Mendapatkan semua departemen dengan jumlah lowongan"""
        dept_list = Departement.objects.all()
        
        if search:
            dept_list = dept_list.filter(nama_dept__icontains=search)
        
        dept_list = dept_list.order_by('nama_dept')
        
        result = []
        for dept in dept_list:
            jumlah_lowongan = Lowongan.objects.filter(departement=dept).count()
            result.append({
                'id': dept.id_dept,
                'nama_dept': dept.nama_dept,
                'jumlah_lowongan': jumlah_lowongan
            })
        
        return result
    
    @staticmethod
    def create_departemen(data):
        """Membuat departemen baru"""
        dept = Departement.objects.create(
            nama_dept=data['nama_dept']
        )
        return dept
    
    @staticmethod
    def update_departemen(id_dept, data):
        """Update departemen yang ada"""
        dept = Departement.objects.get(id_dept=id_dept)
        dept.nama_dept = data['nama_dept']
        dept.save()
        return dept
    
    @staticmethod
    def delete_departemen(id_dept):
        """Hapus departemen"""
        dept = Departement.objects.get(id_dept=id_dept)
        dept.delete()
        return True
    
    @staticmethod
    def get_departemen_by_id(id_dept):
        """Mendapatkan detail departemen berdasarkan ID"""
        dept = Departement.objects.get(id_dept=id_dept)
        return {
            'id': dept.id_dept,
            'nama_dept': dept.nama_dept
        }
    
    @staticmethod
    def get_pending_applicants(search=''):
        """Mendapatkan daftar pendaftar dengan status pending"""
        transaksi_list = TransaksiPendaftaran.objects.select_related(
            'pendaftar', 'lowongan', 'lowongan__departement'
        ).filter(status='pending')
        
        if search:
            transaksi_list = transaksi_list.filter(
                Q(pendaftar__name__icontains=search) |
                Q(lowongan__posisi__icontains=search) |
                Q(pendaftar__university__icontains=search)
            )
        
        transaksi_list = transaksi_list.order_by('-created_at')
        
        result = []
        for transaksi in transaksi_list:
            result.append({
                'id_transaksi': transaksi.id_transaksi_pendaftaran,
                'nama': transaksi.pendaftar.name,
                'nik': transaksi.pendaftar.nik,
                'posisi': transaksi.lowongan.posisi,
                'departemen': transaksi.lowongan.departement.nama_dept,
                'universitas': transaksi.pendaftar.university,
                'jurusan': transaksi.pendaftar.major,
                'ipk': transaksi.pendaftar.ipk,
                'tanggal_daftar': transaksi.created_at.strftime('%d %b %Y')
            })
        
        return result
    
    @staticmethod
    def get_applicants_history(search='', status_filter=''):
        """Mendapatkan riwayat pendaftar (approved/rejected)"""
        transaksi_list = TransaksiPendaftaran.objects.select_related(
            'pendaftar', 'lowongan'
        ).exclude(status='pending')
        
        if status_filter:
            transaksi_list = transaksi_list.filter(status=status_filter)
        
        if search:
            transaksi_list = transaksi_list.filter(
                Q(pendaftar__name__icontains=search) |
                Q(lowongan__posisi__icontains=search)
            )
        
        transaksi_list = transaksi_list.order_by('-updated_at')
        
        result = []
        for transaksi in transaksi_list:
            result.append({
                'id_transaksi': transaksi.id_transaksi_pendaftaran,
                'nama': transaksi.pendaftar.name,
                'posisi': transaksi.lowongan.posisi,
                'tanggal_daftar': transaksi.created_at.strftime('%d %b %Y'),
                'status': transaksi.status
            })
        
        return result
    
    @staticmethod
    def get_applicant_detail(id_transaksi):
        """Mendapatkan detail lengkap pendaftar"""
        transaksi = TransaksiPendaftaran.objects.select_related(
            'pendaftar', 'lowongan', 'lowongan__departement'
        ).get(id_transaksi_pendaftaran=id_transaksi)
        
        pendaftar = transaksi.pendaftar
        
        # Format tanggal lahir
        tanggal_lahir = pendaftar.dob.strftime('%d %B %Y') if pendaftar.dob else '-'
        
        # Format jenis kelamin
        jenis_kelamin_dict = {
            'L': 'Laki-laki',
            'P': 'Perempuan'
        }
        jenis_kelamin = jenis_kelamin_dict.get(pendaftar.gender, pendaftar.gender)
        
        # CV info
        cv_url = None
        cv_filename = None
        if pendaftar.path_cv and pendaftar.path_cv.name:
            try:
                cv_url = pendaftar.path_cv.url
                cv_filename = pendaftar.path_cv.name.split('/')[-1]
            except:
                cv_url = None
                cv_filename = 'CV tidak tersedia'
        
        return {
            'id_transaksi': transaksi.id_transaksi_pendaftaran,
            'nama': pendaftar.name,
            'nik': pendaftar.nik,
            'jenis_kelamin': jenis_kelamin,
            'tanggal_lahir': tanggal_lahir,
            'no_telp': pendaftar.no_telp or '-',
            'alamat': pendaftar.address or '-',
            'universitas': pendaftar.university,
            'jurusan': pendaftar.major,
            'ipk': pendaftar.ipk,
            'posisi': transaksi.lowongan.posisi,
            'departemen': transaksi.lowongan.departement.nama_dept,
            'status': transaksi.status,
            'cv_url': cv_url,
            'cv_filename': cv_filename
        }
    
    @staticmethod
    def update_applicant_status(id_transaksi, status):
        """Update status pendaftar (approve/reject)"""
        if status not in ['approved', 'rejected']:
            raise ValueError('Status harus approved atau rejected')
        
        transaksi = TransaksiPendaftaran.objects.get(id_transaksi_pendaftaran=id_transaksi)
        transaksi.status = status
        transaksi.updated_at = timezone.now()
        transaksi.save()
        
        return transaksi
