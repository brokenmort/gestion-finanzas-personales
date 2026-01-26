from pathlib import Path
import os
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# CLAVES Y DEBUG (LOCAL)
# ======================================================
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-dev-only")
DEBUG = os.environ.get("DEBUG", "True") == "True"

# Solo local
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# ======================================================
# APLICACIONES INSTALADAS
# ======================================================
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "corsheaders",
    "drf_spectacular",

    # Apps locales
    "users",
    "ingresos",
    "egresos",
    "ahorros",
    "prestamos",

    # OJO: en urls.py importas reports.api.views, pero no veo 'reports' en INSTALLED_APPS.
    # Si tienes app 'reports', descomenta:
    # "reports",
]

# ======================================================
# MIDDLEWARE (LOCAL)
# ======================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",

    # CORS antes de CommonMiddleware
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"
ASGI_APPLICATION = "web.asgi.application"

# ======================================================
# BASE DE DATOS (LOCAL)
# ======================================================
# Por defecto SQLite (simple y perfecto para dev)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Si quieres Postgres local más adelante, cambia esto por env vars:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.environ.get("POSTGRES_DB", "mi_db"),
#         "USER": os.environ.get("POSTGRES_USER", "postgres"),
#         "PASSWORD": os.environ.get("POSTGRES_PASSWORD", "postgres"),
#         "HOST": os.environ.get("POSTGRES_HOST", "127.0.0.1"),
#         "PORT": os.environ.get("POSTGRES_PORT", "5432"),
#     }
# }

# ======================================================
# VALIDACIÓN DE CONTRASEÑAS
# ======================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ======================================================
# INTERNACIONALIZACIÓN
# ======================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ======================================================
# DRF + JWT
# ======================================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ======================================================
# CORS / CSRF (LOCAL)
# ======================================================
# Pon aquí el puerto real de tu front (Vite=5173, React=3000, etc.)
FRONTEND_ORIGINS = os.environ.get("FRONTEND_ORIGINS", "http://localhost:5173,http://localhost:3000")
CORS_ALLOWED_ORIGINS = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

# Si usas JWT en headers, no necesitas credenciales/cookies normalmente.
# Pero si en algún punto usas cookies, déjalo en True.
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# ======================================================
# STATIC / MEDIA (LOCAL)
# ======================================================
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ======================================================
# USER MODEL
# ======================================================
AUTH_USER_MODEL = "users.User"

# ======================================================
# EMAIL (LOCAL: consola para no depender de SMTP)
# ======================================================
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ======================================================
# SWAGGER / DOCS
# ======================================================
SPECTACULAR_SETTINGS = {
    "TITLE": "API Local",
    "DESCRIPTION": "Documentación local",
    "VERSION": "0.1.0",
}
