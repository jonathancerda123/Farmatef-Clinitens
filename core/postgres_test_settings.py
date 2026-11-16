"""Pruebas contra el PostgreSQL aislado del laboratorio local."""
from .test_settings import *  # noqa: F403


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "127.0.0.1",
        "PORT": "55432",
        "NAME": "clinitens_qa",
        "USER": "clinitens_qa",
        "PASSWORD": "clinitens_qa_ficticia",
        "CONN_MAX_AGE": 0,
        "OPTIONS": {"options": "-c statement_timeout=15000"},
        "TEST": {"NAME": "test_clinitens_qa"},
    },
}
