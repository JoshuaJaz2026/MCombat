from django.contrib import admin
from django.utils.safestring import mark_safe # <--- CAMBIO AQUÍ: Usamos mark_safe
from .models import Alumno, Asistencia, Pago, Disciplina

# 1. Configuración para Alumnos
class AlumnoAdmin(admin.ModelAdmin):
    # Qué columnas ver
    list_display = ('vista_foto', 'nombre', 'apellido', 'dni', 'fecha_vencimiento', 'estado_pago')
    
    # Esto hace que la FOTO y el NOMBRE sean clics para editar
    list_display_links = ('vista_foto', 'nombre') 
    
    search_fields = ('nombre', 'apellido', 'dni')
    list_filter = ('fecha_vencimiento',)

    # --- SEMÁFORO VISUAL (Corregido con mark_safe) ---
    def estado_pago(self, obj):
        if obj.esta_al_dia():
            # mark_safe funciona perfecto para HTML fijo sin variables extrañas
            return mark_safe('<span style="color: green; font-weight: bold;">✅ Al día</span>')
        return mark_safe('<span style="color: red; font-weight: bold;">❌ Vencido</span>')
    
    estado_pago.short_description = "Estado Membresía"

# 2. Configuración para Pagos
class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'monto', 'fecha_pago', 'fecha_vencimiento', 'mostrar_disciplinas')
    list_filter = ('fecha_pago', 'disciplinas') 
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni')
    autocomplete_fields = ['alumno']
    
    filter_horizontal = ('disciplinas',) 

    def mostrar_disciplinas(self, obj):
        return ", ".join([d.nombre for d in obj.disciplinas.all()])
    mostrar_disciplinas.short_description = "Deportes Pagados"

    class Media:
        css = {
            'all': ('asistencia/parche_cajas.css',)
        }

# 3. Registramos todo
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Asistencia)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Disciplina)