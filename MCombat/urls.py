from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from asistencia import views

urlpatterns = [
    # --- 1. RUTA NUEVA DEL DASHBOARD (¡Debe ir PRIMERO!) ---
    # Si no la pones antes de 'admin/', no funcionará.
    path('admin/dashboard/', views.dashboard_view, name='admin_dashboard'),

    # 2. Panel de Administrador (Va después)
    path('admin/', admin.site.urls),

    # 3. Login y Logout para Entrenadores
    path('login/', auth_views.LoginView.as_view(template_name='login_asistencia.html'), name='login_asistencia'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login_asistencia'), name='logout'),

    # 4. Pantalla de Registro de Asistencia (La Home)
    path('', views.registro_asistencia, name='registro_asistencia'),

    # 5. Exportar Excel
    path('exportar-excel/', views.exportar_alumnos_excel, name='exportar_excel'),

    # --- RUTAS PARA RECUPERAR CONTRASEÑA ---
    path('reset_password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# --- BLOQUE MÁGICO PARA VER LAS FOTOS ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)