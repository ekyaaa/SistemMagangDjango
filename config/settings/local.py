from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Development database (boleh tetap sqlite untuk dev)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
