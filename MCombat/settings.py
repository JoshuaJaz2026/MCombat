"""
Django settings for MCombat project.
"""

from pathlib import Path
import dj_database_url 
import os 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3sq(tx07rnopobikdrgd92b-t7as^4g^k=rfa*@=x4)dzc-k1x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# --- NUEVO: LISTA DE CONFIANZA PARA LOGIN (SOLUCIÓN ERROR 403) ---
CSRF_TRUSTED_ORIGINS = [
    'https://mcombat.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    # --- CLOUDINARY (FOTOS EN LA NUBE) ---
    'cloudinary_storage',  # <--- NUEVO: Para guardar archivos
    'cloudinary',          # <--- NUEVO: La librería base
    # -------------------------------------
    'theme',              # Mantiene tu login con video
    'jazzmin',            # Jazzmin para el diseño admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'asistencia',         # Tu aplicación principal
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'MCombat.urls'

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

WSGI_APPLICATION = 'MCombat.wsgi.application'


# --- BASE DE DATOS (NEON / POSTGRESQL) ---
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://neondb_owner:npg_oK1Ied5hVkCR@ep-dark-queen-a4weiv5e-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require',
        conn_max_age=600
    )
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    { 'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    { 'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]


# Internationalization
LANGUAGE_CODE = 'es-pe'
TIME_ZONE = 'America/Lima'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (CSS, JS, Imágenes del sistema) ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
# NOTA: Se eliminó STATICFILES_STORAGE de aquí porque ahora va en STORAGES (abajo)

# --- ARCHIVOS MEDIA (Fotos de Alumnos) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# ☁️ CONFIGURACIÓN DE CLOUDINARY (FOTOS)
# ==========================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dpl7zq9si', 
    'API_KEY': '593388572931544',
    'API_SECRET': '-HEo5xEFlawCAxuLwQNLkDa8sWs',
}

# ==========================================
# ⚙️ CONFIGURACIÓN MODERNA (DJANGO 5+)
# ==========================================
STORAGES = {
    # 1. Para archivos subidos (Fotos de alumnos) -> Cloudinary
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    # 2. Para archivos del sistema (CSS, JS) -> WhiteNoise
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# CONFIGURACIÓN DE JAZZMIN (Tema y UI)
# ==========================================

JAZZMIN_SETTINGS = {
    "site_title": "MCombat Admin",
    "site_header": "MCombat",
    "site_brand": "MCombat",
    "welcome_sign": "Bienvenido al Panel MCombat",
    "copyright": "MCombat Academy",
    "search_model": "asistencia.Alumno",
    "show_ui_builder": True,

    # --- BOTONES DEL MENÚ SUPERIOR ---
    "topmenu_links": [
        {"name": "Inicio",  "url": "admin:index", "permissions": ["auth.view_user"]},
        {"name": "📊 Ver Estadísticas", "url": "/admin/dashboard/", "new_window": False},
        {"model": "auth.User"},
    ],
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-danger", 
    "accent": "accent-danger", 
    "navbar": "navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-danger",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    
    # --- CAMBIO A TEMA CLARO (FLATLY) ---
    "theme": "flatly",        # Tema blanco moderno
    "dark_mode_theme": None,  # Desactivamos modo oscuro automático
    
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# --- CONFIGURACIÓN DE CORREO (GMAIL / RENDER) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', 'mcombatsoporte@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = 'Soporte MCombat <mcombatsoporte@gmail.com>'