from django.contrib import admin
from django.utils.html import format_html # <--- Importante para los colores
from .models import Alumno, Asistencia, Pago, Disciplina

# 1. Configuración para Alumnos
class AlumnoAdmin(admin.ModelAdmin):
    # Agregamos 'fecha_vencimiento' y el semáforo 'estado_pago'
    list_display = ('vista_foto', 'nombre', 'apellido', 'dni', 'fecha_vencimiento', 'estado_pago')
    
    # --- AQUÍ ESTÁ EL CAMBIO CLAVE ---
    # Esto hace que el NOMBRE tenga enlace azul y puedas hacer clic para editar
    list_display_links = ('vista_foto', 'nombre') 
    # ---------------------------------

    search_fields = ('nombre', 'apellido', 'dni')
    list_filter = ('fecha_vencimiento',) # Filtro lateral para ver quiénes vencen pronto

    # --- SEMÁFORO VISUAL (El Cadenero) ---
    def estado_pago(self, obj):
        # Usamos la función inteligente que creamos en models.py
        if obj.esta_al_dia():
            return format_html('<span style="color: green; font-weight: bold;">✅ Al día</span>')
        return format_html('<span style="color: red; font-weight: bold;">❌ Vencido</span>')
    
    estado_pago.short_description = "Estado Membresía"

# 2. Configuración para Pagos
class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'monto', 'fecha_pago', 'fecha_vencimiento', 'mostrar_disciplinas')
    list_filter = ('fecha_pago', 'disciplinas') 
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni')
    autocomplete_fields = ['alumno'] # Buscador rápido (muy útil cuando tengas 100 alumnos)
    
    filter_horizontal = ('disciplinas',) 

    def mostrar_disciplinas(self, obj):
        return ", ".join([d.nombre for d in obj.disciplinas.all()])
    mostrar_disciplinas.short_description = "Deportes Pagados"

    # Mantenemos tu parche CSS para que las cajas se vean bien
    class Media:
        css = {
            'all': ('asistencia/parche_cajas.css',)
        }

# 3. Registramos todo
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Asistencia)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Disciplina)