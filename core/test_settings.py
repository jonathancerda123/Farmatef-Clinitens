"""Configuración ficticia: nunca importa settings ni lee .env/base/media reales."""
from pathlib import Path
from tempfile import TemporaryDirectory
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "clave-ficticia-exclusiva-de-pruebas-no-para-produccion"
DEBUG = False
ALLOWED_HOSTS = ["testserver", "localhost", "127.0.0.1"]
INSTALLED_APPS = [
    "django.contrib.admin", "django.contrib.auth", "django.contrib.contenttypes",
    "django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles",
    "django.contrib.humanize", "homeApp", "UsuarioApp", "CliniTensDocenteApp",
    "CliniTensFichaApp", "FarmaTEFApp", "CliniTensSimulacionApp", "tailwind", "theme", "allauth", "allauth.account",
    "allauth.mfa", "crispy_forms", "crispy_tailwind", "core.apps.PreventConcurrentLoginsConfig",
    "axes", "django_ckeditor_5",
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "axes.middleware.AxesMiddleware",
    "homeApp.middleware.UpdateLastActivityMiddleware",
    "UsuarioApp.middleware.CambioPasswordObligatorioMiddleware",
]
ROOT_URLCONF = "core.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [BASE_DIR / "templates"], "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.debug",
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
_test_storage = TemporaryDirectory(prefix="clinitens-tests-")
MEDIA_ROOT = Path(_test_storage.name) / "media"
MEDIA_URL = "/media/"
STATIC_URL = "/static/"
STATIC_ROOT = Path(_test_storage.name) / "static"
STATICFILES_DIRS = [BASE_DIR / "static"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
# Servidor de revisión con datos ficticios: solo admite la carpeta de artefactos.
_browser_db = os.environ.get("CLINITENS_TEST_DATABASE")
if _browser_db:
    _db_path = Path(_browser_db).resolve()
    if _db_path.parent != (BASE_DIR / ".test-artifacts").resolve():
        raise ValueError("La base de revisión debe estar en .test-artifacts")
    DATABASES["default"]["NAME"] = str(_db_path)
    MEDIA_ROOT = BASE_DIR / ".test-artifacts" / "media"
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
AUTHENTICATION_BACKENDS = ["axes.backends.AxesStandaloneBackend", "django.contrib.auth.backends.ModelBackend",
                          "allauth.account.auth_backends.AuthenticationBackend"]
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
AUTH_PASSWORD_VALIDATORS = []
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_TZ = True
USE_I18N = True
LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "Home"
ACCOUNT_ADAPTER = "UsuarioApp.adapters.NoSignupAccountAdapter"
ACCOUNT_LOGIN_METHODS = {"username", "email"}
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = False
SESSION_COOKIE_AGE = 1800
TAILWIND_APP_NAME = "theme"
NPM_BIN_PATH = os.environ.get("NPM_BIN_PATH", "npm.cmd" if os.name == "nt" else "npm")
CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"
CRISPY_TEMPLATE_PACK = "tailwind"
CKEDITOR_5_CONFIGS = {"default": {"language": "es"}, "extends": {"language": "es"}}
AXES_ENABLED = False
