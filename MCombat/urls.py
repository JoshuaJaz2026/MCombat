from django.contrib import admin
from django.urls import path
from asistencia.views import registro_asistencia # <--- Importamos tu vista

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registro_asistencia, name='registro_asistencia'), # <--- La dejamos vacía '' para que sea la home
]