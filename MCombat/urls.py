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

# Filtro de correo
from asistencia.forms import ValidarCorreoResetForm 

urlpatterns = [
    # --- 1. ADMIN DE DJANGO ---
    path('admin/', admin.site.urls),

    # --- 2. RUTA INTELIGENTE (SEMÁFORO) ---
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),

    # --- 3. LOGIN OFICIAL ---
    path('login/', auth_views.LoginView.as_view(
            template_name='login_asistencia.html', 
            redirect_authenticated_user=True
        ), name='login_asistencia'),

    # --- 4. TUS RUTAS DE LA APP (DASHBOARD Y REGISTRO) ---
    path('admin/dashboard/', views.dashboard, name='dashboard'), # Esta arregla el error 404
    path('logout/', views.logout, name='logout'), 
    path('', views.registro_asistencia, name='registro_asistencia'),

    # --- 5. REPORTES EXCEL ---
    # Esta es la ruta que usa el botón verde del Dashboard
    path('admin/exportar-excel/', views.exportar_asistencias_excel, name='exportar_excel'),

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