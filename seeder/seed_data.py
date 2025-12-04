import os
import sys
import django
from datetime import datetime, timedelta
from decimal import Decimal

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
django.setup()

from magang.models import Departement, Lowongan, Pendaftar, TransaksiPendaftaran


def clear_data():
    """Hapus semua data existing"""
    print("Menghapus data existing...")
    TransaksiPendaftaran.objects.all().delete()
    Pendaftar.objects.all().delete()
    Lowongan.objects.all().delete()
    Departement.objects.all().delete()
    print("✓ Data existing berhasil dihapus\n")


def seed_departements():
    """Seed data Departemen"""
    print("Seeding Departements...")
    
    departements_data = [
        "Accounting",
        "Business Development",
        "Engineering",
        "Human Resources",
        "Legal",
        "Marketing",
        "Product Management",
        "Sales",
        "Training"
    ]
    
    departements = []
    for nama in departements_data:
        dept = Departement.objects.create(nama_dept=nama)
        departements.append(dept)
        print(f"  ✓ Created: {nama} (ID: {dept.id_dept})")
    
    print(f"✓ {len(departements)} Departements berhasil dibuat\n")
    return departements


def seed_lowongan(departements):
    """Seed data Lowongan"""
    print("Seeding Lowongan...")
    
    today = datetime.now().date()
    
    lowongan_data = [
        {
            "posisi": "Finance Administration Intern",
            "deskripsi": "Membantu proses pembukuan, rekapitulasi data keuangan harian, dan pengarsipan dokumen keuangan perusahaan.",
            "departement": departements[0],  # Accounting
            "tanggal_mulai": today + timedelta(days=15),
            "tanggal_selesai": today + timedelta(days=105)
        },
        {
            "posisi": "Tax Compliance Intern",
            "deskripsi": "Mendukung tim dalam mempersiapkan laporan pajak bulanan dan tahunan serta dokumentasi compliance.",
            "departement": departements[0],  # Accounting
            "tanggal_mulai": today + timedelta(days=30),
            "tanggal_selesai": today + timedelta(days=120)
        },
        {
            "posisi": "Business Analyst Intern",
            "deskripsi": "Melakukan riset pasar, analisis kompetitor, dan menyusun business proposal untuk pengembangan bisnis baru.",
            "departement": departements[1],  # Business Development
            "tanggal_mulai": today + timedelta(days=10),
            "tanggal_selesai": today + timedelta(days=100)
        },
        {
            "posisi": "Partnership Development Intern",
            "deskripsi": "Membantu identifikasi calon mitra strategis dan mempersiapkan presentation deck untuk pitching.",
            "departement": departements[1],  # Business Development
            "tanggal_mulai": today + timedelta(days=20),
            "tanggal_selesai": today + timedelta(days=110)
        },
        {
            "posisi": "Software Engineering Intern",
            "deskripsi": "Pengembangan fitur aplikasi web menggunakan Django dan React, code review, dan testing automation.",
            "departement": departements[2],  # Engineering
            "tanggal_mulai": today + timedelta(days=7),
            "tanggal_selesai": today + timedelta(days=97)
        },
        {
            "posisi": "DevOps Intern",
            "deskripsi": "Membantu deployment aplikasi, monitoring server, dan implementasi CI/CD pipeline.",
            "departement": departements[2],  # Engineering
            "tanggal_mulai": today + timedelta(days=14),
            "tanggal_selesai": today + timedelta(days=104)
        },
        {
            "posisi": "Quality Assurance Intern",
            "deskripsi": "Melakukan testing manual dan automated testing untuk memastikan kualitas software sebelum release.",
            "departement": departements[2],  # Engineering
            "tanggal_mulai": today + timedelta(days=5),
            "tanggal_selesai": today + timedelta(days=95)
        },
        {
            "posisi": "HR Recruitment Intern",
            "deskripsi": "Membantu proses screening CV, penjadwalan interview, dan administrasi rekrutmen karyawan baru.",
            "departement": departements[3],  # Human Resources
            "tanggal_mulai": today + timedelta(days=12),
            "tanggal_selesai": today + timedelta(days=102)
        },
        {
            "posisi": "HR Learning & Development Intern",
            "deskripsi": "Mendukung pelaksanaan program training karyawan dan mempersiapkan materi pelatihan internal.",
            "departement": departements[3],  # Human Resources
            "tanggal_mulai": today + timedelta(days=25),
            "tanggal_selesai": today + timedelta(days=115)
        },
        {
            "posisi": "Legal Research Intern",
            "deskripsi": "Melakukan riset hukum, review kontrak, dan membantu penyusunan legal opinion untuk keperluan bisnis.",
            "departement": departements[4],  # Legal
            "tanggal_mulai": today + timedelta(days=18),
            "tanggal_selesai": today + timedelta(days=108)
        },
        {
            "posisi": "Corporate Legal Intern",
            "deskripsi": "Membantu proses perizinan perusahaan, dokumentasi legal, dan monitoring compliance regulasi.",
            "departement": departements[4],  # Legal
            "tanggal_mulai": today + timedelta(days=28),
            "tanggal_selesai": today + timedelta(days=118)
        },
        {
            "posisi": "Digital Marketing Intern",
            "deskripsi": "Membuat konten untuk social media, mengelola campaign iklan digital, dan analisis engagement metrics.",
            "departement": departements[5],  # Marketing
            "tanggal_mulai": today + timedelta(days=8),
            "tanggal_selesai": today + timedelta(days=98)
        },
        {
            "posisi": "Content Marketing Intern",
            "deskripsi": "Menulis artikel blog, membuat video tutorial, dan mengoptimasi SEO untuk meningkatkan brand awareness.",
            "departement": departements[5],  # Marketing
            "tanggal_mulai": today + timedelta(days=6),
            "tanggal_selesai": today + timedelta(days=96)
        },
        {
            "posisi": "Brand Marketing Intern",
            "deskripsi": "Membantu pelaksanaan event marketing, merchandise design, dan brand campaign activation.",
            "departement": departements[5],  # Marketing
            "tanggal_mulai": today + timedelta(days=22),
            "tanggal_selesai": today + timedelta(days=112)
        },
        {
            "posisi": "Product Manager Intern",
            "deskripsi": "Melakukan user research, membuat product roadmap, dan koordinasi dengan tim engineering untuk development.",
            "departement": departements[6],  # Product Management
            "tanggal_mulai": today + timedelta(days=16),
            "tanggal_selesai": today + timedelta(days=106)
        },
        {
            "posisi": "Product Analyst Intern",
            "deskripsi": "Analisis data pengguna, A/B testing, dan membuat dashboard metrics untuk product performance.",
            "departement": departements[6],  # Product Management
            "tanggal_mulai": today + timedelta(days=11),
            "tanggal_selesai": today + timedelta(days=101)
        },
        {
            "posisi": "Sales Development Intern",
            "deskripsi": "Melakukan prospecting calon klien, cold calling, dan mempersiapkan sales presentation.",
            "departement": departements[7],  # Sales
            "tanggal_mulai": today + timedelta(days=9),
            "tanggal_selesai": today + timedelta(days=99)
        },
        {
            "posisi": "Account Management Intern",
            "deskripsi": "Membantu maintain relationship dengan existing clients dan follow up sales pipeline.",
            "departement": departements[7],  # Sales
            "tanggal_mulai": today + timedelta(days=19),
            "tanggal_selesai": today + timedelta(days=109)
        },
        {
            "posisi": "Corporate Training Intern",
            "deskripsi": "Membantu persiapan dan pelaksanaan program pelatihan internal karyawan serta evaluasi training.",
            "departement": departements[8],  # Training
            "tanggal_mulai": today + timedelta(days=13),
            "tanggal_selesai": today + timedelta(days=103)
        },
        {
            "posisi": "E-Learning Content Developer",
            "deskripsi": "Membuat konten e-learning interaktif, video tutorial, dan modul pelatihan digital.",
            "departement": departements[8],  # Training
            "tanggal_mulai": today + timedelta(days=26),
            "tanggal_selesai": today + timedelta(days=116)
        }
    ]
    
    lowongan_list = []
    for data in lowongan_data:
        lowongan = Lowongan.objects.create(**data)
        lowongan_list.append(lowongan)
        print(f"  ✓ Created: {lowongan.posisi} - {lowongan.departement.nama_dept} (ID: {lowongan.id_lowongan})")
    
    print(f"✓ {len(lowongan_list)} Lowongan berhasil dibuat\n")
    return lowongan_list


def seed_pendaftar(lowongan_list):
    """Seed data Pendaftar"""
    print("Seeding Pendaftar...")
    
    today = datetime.now().date()
    
    pendaftar_data = [
        {
            "lowongan": lowongan_list[0],  # Finance Administration Intern
            "nik": "3273010101950001",
            "name": "Budi Santoso",
            "gender": "L",
            "dob": datetime(1995, 1, 1).date(),
            "address": "Jl. Sudirman No. 123, Jakarta Selatan",
            "no_telp": "081234567890",
            "university": "Universitas Indonesia",
            "major": "Akuntansi",
            "path_cv": "cv/budi_santoso_cv.pdf",
            "ipk": Decimal("3.45")
        },
        {
            "lowongan": lowongan_list[4],  # Software Engineering Intern
            "nik": "3174020202960002",
            "name": "Siti Nurhaliza",
            "gender": "P",
            "dob": datetime(1996, 2, 2).date(),
            "address": "Jl. Gatot Subroto No. 45, Jakarta Pusat",
            "no_telp": "081234567891",
            "university": "Institut Teknologi Bandung",
            "major": "Teknik Informatika",
            "path_cv": "cv/siti_nurhaliza_cv.pdf",
            "ipk": Decimal("3.78")
        },
        {
            "lowongan": lowongan_list[11],  # Digital Marketing Intern
            "nik": "3201030303970003",
            "name": "Ahmad Fauzi",
            "gender": "L",
            "dob": datetime(1997, 3, 3).date(),
            "address": "Jl. Ahmad Yani No. 78, Bogor",
            "no_telp": "081234567892",
            "university": "Universitas Gadjah Mada",
            "major": "Ilmu Komunikasi",
            "path_cv": "cv/ahmad_fauzi_cv.pdf",
            "ipk": Decimal("3.56")
        },
        {
            "lowongan": lowongan_list[7],  # HR Recruitment Intern
            "nik": "3275040404980004",
            "name": "Dewi Lestari",
            "gender": "P",
            "dob": datetime(1998, 4, 4).date(),
            "address": "Jl. Diponegoro No. 56, Bandung",
            "no_telp": "081234567893",
            "university": "Universitas Padjadjaran",
            "major": "Psikologi",
            "path_cv": "cv/dewi_lestari_cv.pdf",
            "ipk": Decimal("3.62")
        },
        {
            "lowongan": lowongan_list[2],  # Business Analyst Intern
            "nik": "3374050505990005",
            "name": "Rizky Pratama",
            "gender": "L",
            "dob": datetime(1999, 5, 5).date(),
            "address": "Jl. Pemuda No. 89, Semarang",
            "no_telp": "081234567894",
            "university": "Universitas Diponegoro",
            "major": "Manajemen",
            "path_cv": "cv/rizky_pratama_cv.pdf",
            "ipk": Decimal("3.71")
        },
        {
            "lowongan": lowongan_list[14],  # Product Manager Intern
            "nik": "3578060600000006",
            "name": "Maya Angelina",
            "gender": "P",
            "dob": datetime(2000, 6, 6).date(),
            "address": "Jl. Basuki Rahmat No. 34, Surabaya",
            "no_telp": "081234567895",
            "university": "Institut Teknologi Sepuluh Nopember",
            "major": "Sistem Informasi",
            "path_cv": "cv/maya_angelina_cv.pdf",
            "ipk": Decimal("3.84")
        },
        {
            "lowongan": lowongan_list[16],  # Sales Development Intern
            "nik": "3471070701010007",
            "name": "Andi Setiawan",
            "gender": "L",
            "dob": datetime(2001, 7, 7).date(),
            "address": "Jl. Pahlawan No. 67, Yogyakarta",
            "no_telp": "081234567896",
            "university": "Universitas Gadjah Mada",
            "major": "Marketing",
            "path_cv": "cv/andi_setiawan_cv.pdf",
            "ipk": Decimal("3.50")
        },
        {
            "lowongan": lowongan_list[9],  # Legal Research Intern
            "nik": "3172080802020008",
            "name": "Putri Wulandari",
            "gender": "P",
            "dob": datetime(2002, 8, 8).date(),
            "address": "Jl. Rasuna Said No. 12, Jakarta Selatan",
            "no_telp": "081234567897",
            "university": "Universitas Indonesia",
            "major": "Hukum",
            "path_cv": "cv/putri_wulandari_cv.pdf",
            "ipk": Decimal("3.68")
        },
        {
            "lowongan": lowongan_list[5],  # DevOps Intern
            "nik": "3273090903030009",
            "name": "Dimas Prasetyo",
            "gender": "L",
            "dob": datetime(2003, 9, 9).date(),
            "address": "Jl. Asia Afrika No. 90, Bandung",
            "no_telp": "081234567898",
            "university": "Institut Teknologi Bandung",
            "major": "Teknik Komputer",
            "path_cv": "cv/dimas_prasetyo_cv.pdf",
            "ipk": Decimal("3.73")
        },
        {
            "lowongan": lowongan_list[18],  # Corporate Training Intern
            "nik": "3201100104040010",
            "name": "Rina Marlina",
            "gender": "P",
            "dob": datetime(2004, 10, 10).date(),
            "address": "Jl. Merdeka No. 23, Bogor",
            "no_telp": "081234567899",
            "university": "Universitas Negeri Jakarta",
            "major": "Pendidikan",
            "path_cv": "cv/rina_marlina_cv.pdf",
            "ipk": Decimal("3.59")
        },
        {
            "lowongan": lowongan_list[12],  # Content Marketing Intern
            "nik": "3174111105050011",
            "name": "Fajar Ramadhan",
            "gender": "L",
            "dob": datetime(2001, 11, 11).date(),
            "address": "Jl. Thamrin No. 45, Jakarta Pusat",
            "no_telp": "081234567800",
            "university": "Universitas Multimedia Nusantara",
            "major": "Desain Komunikasi Visual",
            "path_cv": "cv/fajar_ramadhan_cv.pdf",
            "ipk": Decimal("3.65")
        },
        {
            "lowongan": lowongan_list[1],  # Tax Compliance Intern
            "nik": "3275121206060012",
            "name": "Indah Permatasari",
            "gender": "P",
            "dob": datetime(2000, 12, 12).date(),
            "address": "Jl. Cihampelas No. 78, Bandung",
            "no_telp": "081234567801",
            "university": "Universitas Padjadjaran",
            "major": "Perpajakan",
            "path_cv": "cv/indah_permatasari_cv.pdf",
            "ipk": Decimal("3.81")
        },
        {
            "lowongan": lowongan_list[6],  # Quality Assurance Intern
            "nik": "3374010107070013",
            "name": "Hendra Wijaya",
            "gender": "L",
            "dob": datetime(1999, 1, 13).date(),
            "address": "Jl. Pandanaran No. 56, Semarang",
            "no_telp": "081234567802",
            "university": "Universitas Diponegoro",
            "major": "Sistem Informasi",
            "path_cv": "cv/hendra_wijaya_cv.pdf",
            "ipk": Decimal("3.55")
        },
        {
            "lowongan": lowongan_list[13],  # Brand Marketing Intern
            "nik": "3578020208080014",
            "name": "Citra Dewi",
            "gender": "P",
            "dob": datetime(1998, 2, 14).date(),
            "address": "Jl. Darmo No. 89, Surabaya",
            "no_telp": "081234567803",
            "university": "Universitas Airlangga",
            "major": "Marketing Communication",
            "path_cv": "cv/citra_dewi_cv.pdf",
            "ipk": Decimal("3.70")
        },
        {
            "lowongan": lowongan_list[15],  # Product Analyst Intern
            "nik": "3471030309090015",
            "name": "Bayu Aditya",
            "gender": "L",
            "dob": datetime(1997, 3, 15).date(),
            "address": "Jl. Malioboro No. 12, Yogyakarta",
            "no_telp": "081234567804",
            "university": "Universitas Gadjah Mada",
            "major": "Statistika",
            "path_cv": "cv/bayu_aditya_cv.pdf",
            "ipk": Decimal("3.76")
        }
    ]
    
    pendaftar_list = []
    for data in pendaftar_data:
        pendaftar = Pendaftar.objects.create(**data)
        pendaftar_list.append(pendaftar)
        print(f"  ✓ Created: {pendaftar.name} - {pendaftar.lowongan.posisi} (ID: {pendaftar.id_pendaftar})")
    
    print(f"✓ {len(pendaftar_list)} Pendaftar berhasil dibuat\n")
    return pendaftar_list


def seed_transaksi_pendaftaran(pendaftar_list):
    """Seed data Transaksi Pendaftaran"""
    print("Seeding Transaksi Pendaftaran...")
    
    # Menggunakan ID asli dari pendaftar yang sudah dibuat
    transaksi_data = [
        {
            "pendaftar": pendaftar_list[0],  # Budi Santoso
            "lowongan": pendaftar_list[0].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[1],  # Siti Nurhaliza
            "lowongan": pendaftar_list[1].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[2],  # Ahmad Fauzi
            "lowongan": pendaftar_list[2].lowongan,
            "status": "pending"
        },
        {
            "pendaftar": pendaftar_list[3],  # Dewi Lestari
            "lowongan": pendaftar_list[3].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[4],  # Rizky Pratama
            "lowongan": pendaftar_list[4].lowongan,
            "status": "pending"
        },
        {
            "pendaftar": pendaftar_list[5],  # Maya Angelina
            "lowongan": pendaftar_list[5].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[6],  # Andi Setiawan
            "lowongan": pendaftar_list[6].lowongan,
            "status": "rejected"
        },
        {
            "pendaftar": pendaftar_list[7],  # Putri Wulandari
            "lowongan": pendaftar_list[7].lowongan,
            "status": "pending"
        },
        {
            "pendaftar": pendaftar_list[8],  # Dimas Prasetyo
            "lowongan": pendaftar_list[8].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[9],  # Rina Marlina
            "lowongan": pendaftar_list[9].lowongan,
            "status": "pending"
        },
        {
            "pendaftar": pendaftar_list[10],  # Fajar Ramadhan
            "lowongan": pendaftar_list[10].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[11],  # Indah Permatasari
            "lowongan": pendaftar_list[11].lowongan,
            "status": "approved"
        },
        {
            "pendaftar": pendaftar_list[12],  # Hendra Wijaya
            "lowongan": pendaftar_list[12].lowongan,
            "status": "rejected"
        },
        {
            "pendaftar": pendaftar_list[13],  # Citra Dewi
            "lowongan": pendaftar_list[13].lowongan,
            "status": "pending"
        },
        {
            "pendaftar": pendaftar_list[14],  # Bayu Aditya
            "lowongan": pendaftar_list[14].lowongan,
            "status": "approved"
        }
    ]
    
    transaksi_list = []
    for data in transaksi_data:
        transaksi = TransaksiPendaftaran.objects.create(**data)
        transaksi_list.append(transaksi)
        print(f"  ✓ Created: {transaksi.pendaftar.name} -> {transaksi.lowongan.posisi} [{transaksi.status}] (ID: {transaksi.id_transaksi_pendaftaran})")
    
    print(f"✓ {len(transaksi_list)} Transaksi Pendaftaran berhasil dibuat\n")
    return transaksi_list


def run_seeder():
    """Jalankan semua seeder"""
    print("="*60)
    print("STARTING DATABASE SEEDER")
    print("="*60 + "\n")
    
    try:
        # Clear existing data
        clear_data()
        
        # Seed data
        departements = seed_departements()
        lowongan_list = seed_lowongan(departements)
        pendaftar_list = seed_pendaftar(lowongan_list)
        transaksi_list = seed_transaksi_pendaftaran(pendaftar_list)
        
        print("="*60)
        print("SEEDER COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"Total Departements: {len(departements)}")
        print(f"Total Lowongan: {len(lowongan_list)}")
        print(f"Total Pendaftar: {len(pendaftar_list)}")
        print(f"Total Transaksi: {len(transaksi_list)}")
        print("="*60)
        
    except Exception as e:
        print("\n" + "="*60)
        print("ERROR DURING SEEDING!")
        print("="*60)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_seeder()
