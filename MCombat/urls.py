"""
MCombat URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importamos las vistas
from asistencia import views
from asistencia.views import smart_login_redirect

urlpatterns = [
    # --- 1. ADMIN DE DJANGO ---
    path('admin/', admin.site.urls),

    # --- 2. RUTA INTELIGENTE (SEMÁFORO) ---
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),

    # --- 3. TUS RUTAS DE LA APP (Asistencia) ---
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login_asistencia, name='login_asistencia'),
    path('logout/', views.logout, name='logout'), 
    path('', views.registro_asistencia, name='registro_asistencia'), # Página de inicio
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),

    # --- 4. RECUPERACIÓN DE CONTRASEÑA (CONFIGURADA) ---
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    # === AQUÍ ESTÁ EL CAMBIO CLAVE ===
    # Agregamos success_url='/login/' para que al terminar, vaya al login general.
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(success_url='/login/'), 
         name='password_reset_confirm'),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# Configuración para ver imágenes (Media)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)