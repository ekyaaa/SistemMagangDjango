import os
from .base import *

DEBUG = True  
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
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
SECURE_HSTS_PRELOAD = False
SECURE_SSL_REDIRECT = False