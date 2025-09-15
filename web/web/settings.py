from pathlib import Path
import os
from datetime import timedelta
import dj_database_url

# ======================================================
# RUTAS Y CONFIGURACIÓN BÁSICA
# ======================================================

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================================
# CLAVES Y DEBUG
# ======================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-^j2&dyz6s@hy%b99mn9h@x59ebw%517mflsr^jne%n+ysql@&d"
)
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "pagina-web-finansas-b6474cfcee14.herokuapp.com",
    "pagina-web-finansas.herokuapp.com",
    "gestion-finanzas-personales.herokuapp.com",
    ".herokuapp.com",
    "127.0.0.1",
    "localhost",
    "testserver",
]

_heroku_app = os.environ.get('HEROKU_APP_NAME')
if _heroku_app:
    _host = f"{_heroku_app}.herokuapp.com"
    if _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)

# ======================================================
# APLICACIONES INSTALADAS
# ======================================================

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Terceros
    'drf_yasg',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'django_filters',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',

    # Apps locales
    'users',
    'ingresos',
    'egresos',
    'ahorros',
    'prestamos',
]

# ======================================================
# MIDDLEWARE
# ======================================================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================================================
# URLS Y TEMPLATES
# ======================================================

ROOT_URLCONF = 'web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'web.wsgi.application'

# ======================================================
# BASE DE DATOS
# ======================================================

DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get('DATABASE_URL', f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=600,
    )
}

# ======================================================
# VALIDACIÓN DE CONTRASEÑAS
# ======================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================================================
# INTERNACIONALIZACIÓN
# ======================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================================================
# DJANGO REST FRAMEWORK + JWT
# ======================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
}

# ======================================================
# CORS
# ======================================================

# CORS_ALLOWED_ORIGINS = []

# ======================================================
# ARCHIVOS ESTÁTICOS
# ======================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# ======================================================
# USER MODEL PERSONALIZADO
# ======================================================

AUTH_USER_MODEL = 'users.User'

# ======================================================
# EMAIL
# ======================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

DEFAULT_FROM_EMAIL = os.environ.get(
    'DEFAULT_FROM_EMAIL',
    EMAIL_HOST_USER or f"no-reply@{os.environ.get('HEROKU_APP_NAME', 'localhost')}.herokuapp.com"
)

if os.environ.get('SENDGRID_API_KEY'):
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_API_KEY']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)

# ======================================================
# PK por defecto
# ======================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================================================
# MEDIA
# ======================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

if not DEBUG and not os.environ.get('CLOUDINARY_URL'):
    MEDIA_ROOT = Path('/tmp') / 'media'

# ======================================================
# SWAGGER
# ======================================================

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"',
        }
    },
}

# ======================================================
# STATICFILES STORAGE
# ======================================================

if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

WHITENOISE_USE_FINDERS = True

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CSRF_TRUSTED_ORIGINS = [
    'https://pagina-web-finansas.herokuapp.com',
    'https://pagina-web-finansas-b6474cfcee14.herokuapp.com',
    'https://gestion-finanzas-personales.herokuapp.com',
    'https://*.herokuapp.com',
]

if _heroku_app:
    _origin = f"https://{_heroku_app}.herokuapp.com"
    if _origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(_origin)

# ======================================================
# CLOUDINARY (solo si está configurado)
# ======================================================

_cloudinary_url = os.environ.get("CLOUDINARY_URL")
if _cloudinary_url:
    if 'cloudinary_storage' not in INSTALLED_APPS:
        INSTALLED_APPS.insert(INSTALLED_APPS.index('django.contrib.staticfiles'), 'cloudinary_storage')
    if 'cloudinary' not in INSTALLED_APPS:
        INSTALLED_APPS.append('cloudinary')

    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
