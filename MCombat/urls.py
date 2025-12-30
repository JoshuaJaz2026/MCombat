from django.contrib import admin
from django.urls import path
from asistencia.views import registro_asistencia # <--- Importamos tu vista
from asistencia import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registro_asistencia, name='registro_asistencia'), # <--- La dejamos vacía '' para que sea la home
    path('exportar-excel/', views.exportar_alumnos_excel, name='exportar_excel'),
]

