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
    # --- 1. RUTAS PERSONALIZADAS DEL ADMIN (¡VAN PRIMERO!) ---
    # Deben ir antes de admin.site.urls para que Django no las confunda
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/exportar-excel/', views.exportar_asistencias_excel, name='exportar_excel'),

    # --- 2. ADMIN OFICIAL DE DJANGO ---
    path('admin/', admin.site.urls),

    # --- 3. RUTA INTELIGENTE (SEMÁFORO) ---
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),

    # --- 4. LOGIN ---
    path('login/', auth_views.LoginView.as_view(
            template_name='login_asistencia.html', 
            redirect_authenticated_user=True
        ), name='login_asistencia'),

    # --- 5. OTRAS RUTAS ---
    path('logout/', views.logout, name='logout'), 
    path('', views.registro_asistencia, name='registro_asistencia'),

    # --- 6. RECUPERACIÓN DE CONTRASEÑA ---
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