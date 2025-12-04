from django.db.models import Q
from django.core.exceptions import ValidationError
from ..models import Lowongan, Pendaftar, TransaksiPendaftaran

class TransaksiPendaftaranService:
    """Service untuk mengelola CRUD Transaksi Pendaftaran (Admin)"""
    
    @staticmethod
    def get_all_transaksi():
        """Mendapatkan semua transaksi pendaftaran"""
        return TransaksiPendaftaran.objects.select_related(
            'pendaftar', 'lowongan', 'lowongan__departement'
        ).order_by('-created_at')
    
    @staticmethod
    def get_transaksi_by_id(id_transaksi):
        """Mendapatkan detail transaksi berdasarkan ID"""
        try:
            return TransaksiPendaftaran.objects.select_related(
                'pendaftar', 'lowongan', 'lowongan__departement'
            ).get(id_transaksi_pendaftaran=id_transaksi)
        except TransaksiPendaftaran.DoesNotExist:
            return None
    
    @staticmethod
    def get_transaksi_by_status(status):
        """Mendapatkan transaksi berdasarkan status"""
        return TransaksiPendaftaran.objects.select_related(
            'pendaftar', 'lowongan', 'lowongan__departement'
        ).filter(status=status).order_by('-created_at')
    
    @staticmethod
    def update_status_transaksi(id_transaksi, new_status):
        """
        Mengubah status transaksi pendaftaran
        Args:
            id_transaksi (int): ID transaksi
            new_status (str): Status baru ('pending', 'approved', 'rejected')
        Returns:
            dict: {'success': bool, 'transaksi': TransaksiPendaftaran, 'message': str}
        """
        valid_statuses = ['pending', 'approved', 'rejected']
        
        if new_status not in valid_statuses:
            return {
                'success': False,
                'transaksi': None,
                'message': f'Status tidak valid. Pilih dari: {", ".join(valid_statuses)}'
            }
        
        try:
            transaksi = TransaksiPendaftaran.objects.get(id_transaksi_pendaftaran=id_transaksi)
            old_status = transaksi.status
            transaksi.status = new_status
            transaksi.save()
            
            return {
                'success': True,
                'transaksi': transaksi,
                'message': f'Status berhasil diubah dari {old_status} ke {new_status}'
            }
        except TransaksiPendaftaran.DoesNotExist:
            return {
                'success': False,
                'transaksi': None,
                'message': 'Transaksi tidak ditemukan'
            }
        except Exception as e:
            return {
                'success': False,
                'transaksi': None,
                'message': f'Terjadi kesalahan: {str(e)}'
            }
    
    @staticmethod
    def delete_transaksi(id_transaksi):
        """
        Menghapus transaksi pendaftaran
        Args:
            id_transaksi (int): ID transaksi yang akan dihapus
        Returns:
            dict: {'success': bool, 'message': str}
        """
        try:
            transaksi = TransaksiPendaftaran.objects.get(id_transaksi_pendaftaran=id_transaksi)
            pendaftar_name = transaksi.pendaftar.name
            lowongan_posisi = transaksi.lowongan.posisi
            
            transaksi.delete()
            
            return {
                'success': True,
                'message': f'Transaksi pendaftaran {pendaftar_name} untuk {lowongan_posisi} berhasil dihapus'
            }
        except TransaksiPendaftaran.DoesNotExist:
            return {
                'success': False,
                'message': 'Transaksi tidak ditemukan'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Terjadi kesalahan: {str(e)}'
            }
    
    @staticmethod
    def create_transaksi_manual(id_pendaftar, id_lowongan, status='pending'):
        """
        Membuat transaksi pendaftaran secara manual (untuk admin)
        Args:
            id_pendaftar (int): ID pendaftar yang sudah ada
            id_lowongan (int): ID lowongan
            status (str): Status awal transaksi
        Returns:
            dict: {'success': bool, 'transaksi': TransaksiPendaftaran, 'message': str}
        """
        try:
            pendaftar = Pendaftar.objects.get(id_pendaftar=id_pendaftar)
            lowongan = Lowongan.objects.get(id_lowongan=id_lowongan)
            
            # Cek duplikasi
            existing = TransaksiPendaftaran.objects.filter(
                pendaftar=pendaftar,
                lowongan=lowongan
            ).first()
            
            if existing:
                return {
                    'success': False,
                    'transaksi': None,
                    'message': f'Transaksi sudah ada dengan status {existing.status}'
                }
            
            transaksi = TransaksiPendaftaran.objects.create(
                pendaftar=pendaftar,
                lowongan=lowongan,
                status=status
            )
            
            return {
                'success': True,
                'transaksi': transaksi,
                'message': 'Transaksi berhasil dibuat'
            }
            
        except Pendaftar.DoesNotExist:
            return {
                'success': False,
                'transaksi': None,
                'message': 'Pendaftar tidak ditemukan'
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
