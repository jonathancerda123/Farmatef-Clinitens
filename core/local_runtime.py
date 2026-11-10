"""Uso local explícito con base restaurada; no importa datos/config de pruebas."""
import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Esta configuración omite .env para no depender de secretos de otra copia.
os.environ["CLINITENS_READ_ENV"] = "0"
from .settings import *  # noqa: E402,F403

_local_root = Path(__file__).resolve().parent.parent
_secret_file = _local_root / ".test-artifacts" / "original-021" / "local-secret.key"
if not _secret_file.is_file() or not (_local_root / "db.sqlite3").is_file():
    raise ImproperlyConfigured("Prepara primero la base local respaldada y su clave privada según docs/ENTORNO_Y_VERIFICACION.md.")

SECRET_KEY = _secret_file.read_text(encoding="utf-8").strip()
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": _local_root / "db.sqlite3"}}
SESSION_COOKIE_NAME = "clinitens_local_session"
CSRF_COOKIE_NAME = "clinitens_local_csrf"
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
