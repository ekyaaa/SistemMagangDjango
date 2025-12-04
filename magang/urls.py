from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/lowongan/', views.get_lowongan_api, name='get_lowongan_api'),
    path('api/submit-pendaftaran/', views.submit_pendaftaran, name='submit_pendaftaran'),
]