from django.db.models import Q
from ..models import Lowongan


class LowonganService:
    """Service untuk mengelola Lowongan (List & Search)"""
    
    @staticmethod
    def get_all_lowongan():
        """Mendapatkan semua lowongan dengan relasi departement"""
        return Lowongan.objects.select_related('departement').order_by('-tanggal_mulai')
    
    @staticmethod
    def search_lowongan(query):
        """
        Mencari lowongan berdasarkan posisi atau nama departemen
        Args:
            query (str): kata kunci pencarian
        Returns:
            QuerySet: Hasil pencarian lowongan
        """
        if not query:
            return LowonganService.get_all_lowongan()
        
        return Lowongan.objects.select_related('departement').filter(
            Q(posisi__icontains=query) | 
            Q(departement__nama_dept__icontains=query)
        ).order_by('-tanggal_mulai')
    
    @staticmethod
    def get_lowongan_by_id(id_lowongan):
        """Mendapatkan detail lowongan berdasarkan ID"""
        try:
            return Lowongan.objects.select_related('departement').get(id_lowongan=id_lowongan)
        except Lowongan.DoesNotExist:
            return None

