"""
MCombat URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importamos las vistas de tu app 'asistencia'
from asistencia import views
from asistencia.views import smart_login_redirect

urlpatterns = [
    # --- 1. NUEVA RUTA INTELIGENTE ---
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),

    # --- 2. ADMIN DE DJANGO (¡Esto es lo que faltaba!) ---
    path('admin/', admin.site.urls),

    # --- 3. TUS RUTAS DE LA APP (Restauradas) ---
    # Estas son las que tenías antes. Si alguna da error, avísame.
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_asistencia, name='login_asistencia'),
    path('logout/', views.logout, name='logout'), # A veces se llama 'logout_view', prueba 'logout' primero
    path('', views.registro_asistencia, name='registro_asistencia'),
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),

    # --- 4. RECUPERACIÓN DE CONTRASEÑA (Brevo) ---
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Configuración para ver imágenes en modo desarrollo/producción
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)