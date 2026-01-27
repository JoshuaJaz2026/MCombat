"""
MCombat URL Configuration
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

# Importamos las vistas
from asistencia import views
from asistencia.views import smart_login_redirect
from asistencia.forms import ValidarCorreoResetForm 

urlpatterns = [
    # ==============================================================================
    # 1. RUTAS PERSONALIZADAS DEL ADMIN (DASHBOARD Y EXCEL)
    # ==============================================================================
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/exportar-excel/', views.exportar_asistencias_excel, name='exportar_excel'),

    # ==============================================================================
    # 2. 🔥 CORRECCIÓN: LOGOUT DEL ADMIN (INTERCEPTOR)
    # Esta línea obliga a que si sales del Admin, vuelvas al login MORADO (/admin/login/)
    # y no al rojo. Debe ir ANTES de admin.site.urls
    # ==============================================================================
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='/admin/login/'), name='admin_logout'),

    # ==============================================================================
    # 3. ADMIN OFICIAL DE DJANGO
    # ==============================================================================
    path('admin/', admin.site.urls),

    # ==============================================================================
    # 4. RUTAS DEL SISTEMA DE ASISTENCIA
    # ==============================================================================
    
    # Consulta Pública
    path('consulta/', views.consulta_publica, name='consulta_publica'),

    # Ruta Inteligente (Semáforo)
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),

    # Login Rojo (Staff/Asistencia)
    path('login/', auth_views.LoginView.as_view(
            template_name='login_asistencia.html', 
            redirect_authenticated_user=True
        ), name='login_asistencia'),

    # Logout Rojo (Staff) - Este usa la configuración global de settings.py
    path('logout/', views.logout, name='logout'), 
    
    # Pantalla Principal (Registro)
    path('', views.registro_asistencia, name='registro_asistencia'),

    # ==============================================================================
    # 5. RECUPERACIÓN DE CONTRASEÑA
    # ==============================================================================
    path('reset_password/', 
         auth_views.PasswordResetView.as_view(
             form_class=ValidarCorreoResetForm
         ), 
         name='password_reset'),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(success_url='/login/'), 
         name='password_reset_confirm'),
    
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)