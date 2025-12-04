from django.db.models import Q
from ..models import Lowongan, Pendaftar, TransaksiPendaftaran

class PendaftaranService:
    """Service untuk mengelola proses pendaftaran"""
    
    @staticmethod
    def check_nik_exists(nik):
        """
        Mengecek apakah NIK sudah terdaftar
        Args:
            nik (str): NIK yang akan dicek
        Returns:
            dict: {'exists': bool, 'pendaftar': Pendaftar atau None}
        """
        try:
            pendaftar = Pendaftar.objects.get(nik=nik)
            return {
                'exists': True,
                'pendaftar': pendaftar,
                'message': f'NIK {nik} sudah terdaftar atas nama {pendaftar.name}'
            }
        except Pendaftar.DoesNotExist:
            return {
                'exists': False,
                'pendaftar': None,
                'message': 'NIK belum terdaftar'
            }
    
    @staticmethod
    def check_duplicate_application(nik, id_lowongan):
        """
        Mengecek apakah NIK sudah mendaftar pada lowongan tertentu
        Args:
            nik (str): NIK pendaftar
            id_lowongan (int): ID lowongan
        Returns:
            dict: {'exists': bool, 'transaksi': TransaksiPendaftaran atau None}
        """
        try:
            pendaftar = Pendaftar.objects.get(nik=nik)
            transaksi = TransaksiPendaftaran.objects.filter(
                pendaftar=pendaftar,
                lowongan_id=id_lowongan
            ).first()
            
            if transaksi:
                return {
                    'exists': True,
                    'transaksi': transaksi,
                    'message': f'NIK {nik} sudah mendaftar pada lowongan ini dengan status {transaksi.status}'
                }
            return {
                'exists': False,
                'transaksi': None,
                'message': 'Belum pernah mendaftar pada lowongan ini'
            }
        except Pendaftar.DoesNotExist:
            return {
                'exists': False,
                'transaksi': None,
                'message': 'NIK belum terdaftar'
            }
    
    @staticmethod
    def create_pendaftaran(data):
        """
        Membuat pendaftaran baru (Pendaftar + TransaksiPendaftaran)
        Args:
            data (dict): Data pendaftar dan lowongan
                - nik, name, gender, dob, address, no_telp
                - university, major, ipk, path_cv
                - id_lowongan
        Returns:
            dict: {'success': bool, 'transaksi': TransaksiPendaftaran, 'message': str}
        """
        try:
            # 1. Cek apakah NIK sudah terdaftar
            nik_check = PendaftaranService.check_nik_exists(data['nik'])
            
            if nik_check['exists']:
                # NIK sudah ada, cek apakah sudah mendaftar di lowongan yang sama
                duplicate_check = PendaftaranService.check_duplicate_application(
                    data['nik'], 
                    data['id_lowongan']
                )
                
                if duplicate_check['exists']:
                    return {
                        'success': False,
                        'transaksi': None,
                        'message': f'NIK sudah terdaftar pada lowongan ini dengan status {duplicate_check["transaksi"].status}'
                    }
                
                # NIK ada tapi belum daftar di lowongan ini, gunakan pendaftar yang ada
                pendaftar = nik_check['pendaftar']
            else:
                # NIK belum ada, buat pendaftar baru
                pendaftar = Pendaftar.objects.create(
                    nik=data['nik'],
                    name=data['name'],
                    gender=data['gender'],
                    dob=data['dob'],
                    address=data['address'],
                    no_telp=data['no_telp'],
                    university=data['university'],
                    major=data['major'],
                    ipk=data.get('ipk'),
                    path_cv=data['path_cv']
                )
            
            # 2. Ambil lowongan
            lowongan = Lowongan.objects.get(id_lowongan=data['id_lowongan'])
            
            # 3. Buat transaksi pendaftaran
            transaksi = TransaksiPendaftaran.objects.create(
                pendaftar=pendaftar,
                lowongan=lowongan,
                status='pending'
            )
            
            return {
                'success': True,
                'transaksi': transaksi,
                'pendaftar': pendaftar,
                'message': 'Pendaftaran berhasil dibuat dengan status pending'
            }
            
        except Lowongan.DoesNotExist:
            return {
                'success': False,
                'transaksi': None,
                'message': 'Lowongan tidak ditemukan'
            }
        except Exception as e:
            return {
                'success': False,
                'transaksi': None,
                'message': f'Terjadi kesalahan: {str(e)}'
            }

