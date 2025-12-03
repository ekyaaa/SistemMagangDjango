from django.db import models
    
# Create your models here.
class Departement(models.Model):
    id_dept = models.AutoField(primary_key=True)
    nama_dept = models.CharField(max_length=100)

    class Meta:
        db_table = 'm_dept'
        verbose_name = 'Departement'
        verbose_name_plural = 'Departements'


class Lowongan(models.Model):
    id_lowongan = models.AutoField(primary_key=True)
    posisi = models.CharField(max_length=255)
    deskripsi = models.CharField(max_length=512)
    tanggal_mulai = models.DateField()
    tanggal_selesai = models.DateField()
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)


    class Meta:
        db_table = 'magang_table'  
        verbose_name = 'Lowongan'
        verbose_name_plural = 'Lowongan'

        ordering = ['tanggal_mulai']  
        indexes = [
            models.Index(fields=['tanggal_mulai', 'departement']),
        ]

    def __str__(self):
        return f"{self.posisi} - {self.departement.nama_dept}"


class Pendaftar(models.Model):
    id_pendaftar = models.AutoField(primary_key=True)
    lowongan = models.ForeignKey(Lowongan, on_delete=models.CASCADE, related_name='pendaftar')
    nik = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=[('L', 'Laki-laki'), ('P', 'Perempuan')])
    dob = models.DateField(verbose_name="Tanggal Lahir")
    address = models.TextField()
    no_telp = models.CharField(max_length=20)
    university = models.CharField(max_length=255)
    major = models.CharField(max_length=255)
    path_cv = models.FileField(upload_to='cv/')  
    ipk = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pendaftar'
        verbose_name = 'Pendaftar'
        verbose_name_plural = 'Pendaftar'
        ordering = ['-created_at']  

    def __str__(self):
        return f"{self.name} - {self.nik}"


class TransaksiPendaftaran(models.Model):
    id_transaksi_pendaftaran = models.AutoField(primary_key=True)
    pendaftar = models.ForeignKey(Pendaftar, on_delete=models.CASCADE, related_name='transaksi_pendaftaran')
    lowongan = models.ForeignKey(Lowongan, on_delete=models.CASCADE, related_name='transaksi_pendaftaran')
    status = models.CharField(
        max_length=50,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)      

    class Meta:
        db_table = 't_pendaftaran_magang'
        verbose_name = 'Transaksi Pendaftaran'
        verbose_name_plural = 'Transaksi Pendaftaran'
        ordering = ['-created_at']  

    def __str__(self):
        return f"{self.pendaftar.name} - {self.lowongan.posisi} ({self.status})"
