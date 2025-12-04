from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('manajemen-lowongan/', views.manajemen_lowongan, name='manajemen_lowongan'),
    path('manajemen-pendaftar/', views.manajemen_pendaftar, name='manajemen_pendaftar'),
    path('api/stats/', views.get_dashboard_stats, name='dashboard_stats'),
    path('api/trend/', views.get_trend_chart_data, name='trend_data'),
    path('api/department/', views.get_department_chart_data, name='department_data'),
    path('api/recent-applicants/', views.get_recent_applicants, name='recent_applicants'),
    
    # CRUD Lowongan
    path('api/lowongan/', views.api_lowongan_list, name='api_lowongan_list'),
    path('api/lowongan/create/', views.api_lowongan_create, name='api_lowongan_create'),
    path('api/lowongan/<int:id_lowongan>/', views.api_lowongan_detail, name='api_lowongan_detail'),
    path('api/lowongan/<int:id_lowongan>/update/', views.api_lowongan_update, name='api_lowongan_update'),
    path('api/lowongan/<int:id_lowongan>/delete/', views.api_lowongan_delete, name='api_lowongan_delete'),
    
    # CRUD Departemen
    path('api/departemen/', views.api_departemen_list, name='api_departemen_list'),
    path('api/departemen/create/', views.api_departemen_create, name='api_departemen_create'),
    path('api/departemen/<int:id_dept>/', views.api_departemen_detail, name='api_departemen_detail'),
    path('api/departemen/<int:id_dept>/update/', views.api_departemen_update, name='api_departemen_update'),
    path('api/departemen/<int:id_dept>/delete/', views.api_departemen_delete, name='api_departemen_delete'),
    
    # Pendaftar Management
    path('api/pendaftar/pending/', views.api_pendaftar_pending, name='api_pendaftar_pending'),
    path('api/pendaftar/history/', views.api_pendaftar_history, name='api_pendaftar_history'),
    path('api/pendaftar/detail/<int:id_transaksi>/', views.api_pendaftar_detail, name='api_pendaftar_detail'),
    path('api/pendaftar/<int:id_transaksi>/update-status/', views.api_pendaftar_update_status, name='api_pendaftar_update_status'),
]
