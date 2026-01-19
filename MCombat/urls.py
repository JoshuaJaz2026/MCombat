from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from asistencia import views  # Importamos tus vistas (incluyendo el dashboard)

urlpatterns = [
    # --- 1. RUTA NUEVA DEL DASHBOARD (¡Debe ir PRIMERO!) ---
    # Al ponerla aquí, interceptamos la url antes de que entre al admin normal
    path('admin/dashboard/', views.dashboard_view, name='dashboard'),

    # 2. Panel de Administrador (Va después)
    path('admin/', admin.site.urls),

    # 3. Login y Logout para Staff
    path('login/', auth_views.LoginView.as_view(template_name='login_asistencia.html'), name='login_asistencia'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_asistencia'), name='logout'),

    # 4. Pantalla de Registro de Asistencia (La Home / Scanner)
    path('', views.registro_asistencia, name='registro_asistencia'),

    # 5. Exportar Excel
    path('exportar-excel/', views.exportar_alumnos_excel, name='exportar_excel'),

    # --- RUTAS PARA RECUPERAR CONTRASEÑA ---
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# --- BLOQUE MÁGICO PARA VER LAS FOTOS (Modo Debug) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # MCombat/urls.py

# 1. Asegúrate de importar la vista nueva arriba
from asistencia.views import smart_login_redirect 

urlpatterns = [
    # ... tus otras rutas ...
    
    # 2. Agrega esta ruta especial
    path('smart-redirect/', smart_login_redirect, name='smart_redirect'),
]