from pathlib import Path
import os
from datetime import timedelta

# ======================================================
# RUTAS Y CONFIGURACIÓN BÁSICA
# ======================================================

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

    # Si sigues usando drf_yasg en vistas, puedes dejarlo instalado.
    # Pero en local no es necesario.
    "drf_yasg",

    # Apps locales
    "users",
    "ingresos",
    "egresos",
    "ahorros",
    "prestamos",

    # OJO: en urls.py importas reports.api.views.
    # Si tienes app reports, descomenta:
    # "reports",
]

# ======================================================
# MIDDLEWARE
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

# ======================================================
# URLS Y TEMPLATES
# ======================================================

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
# BASE DE DATOS (LOCAL LIMPIA)
# ======================================================

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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
# DJANGO REST FRAMEWORK + JWT
# ======================================================

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # ✅ Esto hace que todo el API acepte JSON por defecto
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
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

# Cambia/añade los puertos que uses para tu front
FRONTEND_ORIGINS = os.environ.get(
    "FRONTEND_ORIGINS",
    "http://localhost:5173,http://localhost:3000,"
    "http://127.0.0.1:5173,http://127.0.0.1:3000,"
    "http://localhost:5500,http://127.0.0.1:5500"
)

CORS_ALLOWED_ORIGINS = [o.strip() for o in FRONTEND_ORIGINS.split(",") if o.strip()]

# Para JWT por header, esto puede estar True o False; no afecta el preflight.
CORS_ALLOW_CREDENTIALS = True

# (Opcional) CSRF no aplica si solo usas JWT en Authorization, pero no estorba.
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
]

# ======================================================
# ARCHIVOS ESTÁTICOS (LOCAL)
# ======================================================

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ======================================================
# MEDIA (LOCAL)
# ======================================================

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ======================================================
# USER MODEL PERSONALIZADO
# ======================================================

AUTH_USER_MODEL = "users.User"

# ======================================================
# EMAIL (LOCAL: imprimir en consola)
# ======================================================

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@localhost")

# ======================================================
# DOCS (drf-spectacular)
# ======================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "API Local",
    "DESCRIPTION": "Documentación local",
    "VERSION": "0.1.0",
}
