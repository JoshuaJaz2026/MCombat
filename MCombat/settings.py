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

# --- LISTA DE CONFIANZA PARA LOGIN ---
CSRF_TRUSTED_ORIGINS = [
    'https://mcombat.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    # --- CLOUDINARY ---
    'cloudinary_storage',
    'cloudinary',
    # ------------------
    'theme',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'asistencia',
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


# --- BASE DE DATOS ---
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


# --- ARCHIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# --- ARCHIVOS MEDIA ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==========================================
# ☁️ CONFIGURACIÓN DE CLOUDINARY
# ==========================================
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dpl7zq9si', 
    'API_KEY': '593388572931544',
    'API_SECRET': '-HEo5xEFIaWCAxuLwQNLeDa8sWs',
}

# ==========================================
# 🚑 PARCHE DE COMPATIBILIDAD
# ==========================================
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# ==========================================
# ⚙️ CONFIGURACIÓN MODERNA (DJANGO 5+)
# ==========================================
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==========================================
# CONFIGURACIÓN DE JAZZMIN
# ==========================================

JAZZMIN_SETTINGS = {
    "site_title": "MCombat Admin",
    "site_header": "MCombat",
    "site_brand": "MCombat",
    "welcome_sign": "Bienvenido al Panel MCombat",
    "copyright": "MCombat Academy",
    "search_model": "asistencia.Alumno",
    "show_ui_builder": True,

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
    
    "theme": "flatly",
    "dark_mode_theme": None,
    
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# ==========================================
# 📧 CONFIGURACIÓN DE CORREO (FINAL)
# ==========================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.brevo.com'
EMAIL_PORT = 2525  # Mantenemos 2525 que ya vimos que no tiene bloqueo
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_TIMEOUT = 30

# 1. USUARIO SMTP (EL CÓDIGO ESPECIAL DE BREVO)
# ¡Este es el que funcionó!
EMAIL_HOST_USER = 'a04a45001@smtp-brevo.com'

# 2. CONTRASEÑA (La clave API que ya tienes en Render)
# Usamos .strip() por seguridad para limpiar espacios invisibles
brevo_key = os.environ.get('BREVO_API_KEY', '')
EMAIL_HOST_PASSWORD = brevo_key.strip()

# 3. REMITENTE (Esto es lo que ven los alumnos)
DEFAULT_FROM_EMAIL = 'Soporte MCombat <mcombatsoporte@gmail.com>'

# ==========================================
# 🧭 REDIRECCIONES DE LOGIN (MAPA DE NAVEGACIÓN)
# ==========================================

# 1. ¿Dónde está tu página de Login? (Para evitar error 404 buscando /accounts/login/)
LOGIN_URL = '/login/'

# 2. ¿A dónde ir después de iniciar sesión correctamente?
LOGIN_REDIRECT_URL =