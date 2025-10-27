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
    "SECRET_KEY",  # usa SECRET_KEY estándar en Render
    "django-insecure-dev-only"
)
DEBUG = os.environ.get("DEBUG", "False") == "True"

# ALLOWED_HOSTS:
# - Siempre permitimos localhost para desarrollo
# - Añadimos Render automáticamente (si lo deseas). Mejor controla por ENV.
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
# Permite añadir múltiples hosts separados por comas desde ENV:
#   ALLOWED_HOSTS=api-miapp.onrender.com,mi-dominio.com
_env_allowed = os.environ.get("ALLOWED_HOSTS")
if _env_allowed:
    ALLOWED_HOSTS += [h.strip() for h in _env_allowed.split(",") if h.strip()]

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

# Render inyecta DATABASE_URL al enlazar Postgres. Si no existe, usa sqlite.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=True  # en Postgres gestionado conviene exigir SSL
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
# CORS / CSRF (controlados por ENV para no tocar código)
# ======================================================

# FRONTEND_ORIGINS="https://mi-front.pages.dev,https://mi-dominio.com"
_frontends = [o.strip() for o in os.environ.get("FRONTEND_ORIGINS", "").split(",") if o.strip()]

CORS_ALLOWED_ORIGINS = _frontends
CORS_ALLOW_CREDENTIALS = True  # por si usas cookies; si solo usas JWT no afecta

# CSRF_TRUSTED_ORIGINS requiere esquema (https://)
# CSRF_TRUSTED_ORIGINS="https://mi-front.pages.dev,https://mi-dominio.com"
CSRF_TRUSTED_ORIGINS = _frontends

# ======================================================
# ARCHIVOS ESTÁTICOS
# ======================================================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / "static"]
# En producción: archivos comprimidos + nombres con hash para cacheo
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_USE_FINDERS = True

# ======================================================
# MEDIA
# ======================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
# En contenedores efímeros, puedes redirigir a /tmp si no usas CLOUDINARY
if not DEBUG and not os.environ.get('CLOUDINARY_URL'):
    MEDIA_ROOT = Path('/tmp') / 'media'

# ======================================================
# USER MODEL PERSONALIZADO
# ======================================================

AUTH_USER_MODEL = 'users.User'

# ======================================================
# EMAIL (sin referencias a Heroku)
# ======================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', "587"))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', "True") == "True"
EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', EMAIL_HOST_USER or "no-reply@localhost")

# Soporte SendGrid si proporcionas la API key
if os.environ.get('SENDGRID_API_KEY'):
    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'apikey'
    EMAIL_HOST_PASSWORD = os.environ['SENDGRID_API_KEY']
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', DEFAULT_FROM_EMAIL)

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
# PROXY/HTTPS
# ======================================================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ======================================================
# CLOUDINARY (opcional)
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
