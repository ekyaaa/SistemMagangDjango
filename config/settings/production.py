import os
from .base import *

DEBUG = False 
ALLOWED_HOSTS = ["yourdomain.com", "localhost", "127.0.0.1", "[::1]"]

# Database PostgreSQL

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'sistem_magang_django',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',  
        'PORT': '5432'
    }
}

# Security settings
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
