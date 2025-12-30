from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from .models import Alumno, Asistencia, Pago

class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'dni', 'telefono')
    search_fields = ('nombre', 'apellido', 'dni')

class AsistenciaAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha')
    list_filter = ('fecha', 'alumno')
    date_hierarchy = 'fecha'

class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'fecha_pago', 'fecha_vencimiento', 'estado_pago')
    search_fields = ('alumno__nombre', 'alumno__dni')
    
    # --- CORRECCIÓN AQUÍ ---
    # Usamos {} como marcador y pasamos el texto después de la coma.
    def estado_pago(self, obj):
        if obj.fecha_vencimiento >= timezone.now().date():
            return format_html('<span style="color:green; font-weight:bold;">{}</span>', "✅ ACTIVO")
        else:
            return format_html('<span style="color:red; font-weight:bold;">{}</span>', "❌ VENCIDO")

admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Asistencia, AsistenciaAdmin)
admin.site.register(Pago, PagoAdmin)