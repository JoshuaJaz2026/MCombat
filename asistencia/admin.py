from django.contrib import admin
from django.utils import timezone
from .models import Alumno, Asistencia, Pago, Disciplina

# 1. Configuración para Alumnos
class AlumnoAdmin(admin.ModelAdmin):
    # Agregamos 'ver_disciplinas_activas' a la lista
    list_display = ('vista_foto', 'nombre', 'apellido', 'dni', 'telefono', 'ver_disciplinas_activas')
    search_fields = ('nombre', 'apellido', 'dni')

    # --- FUNCIÓN ESPÍA: Busca qué entrena el alumno HOY ---
    def ver_disciplinas_activas(self, obj):
        hoy = timezone.now().date()
        
        # Buscamos el último pago VÁLIDO (que no haya vencido)
        pago_activo = Pago.objects.filter(
            alumno=obj, 
            fecha_vencimiento__gte=hoy
        ).order_by('-fecha_vencimiento').first()

        if pago_activo:
            # Si tiene pago, sacamos la lista de sus deportes
            deportes = [d.nombre for d in pago_activo.disciplinas.all()]
            return ", ".join(deportes) # Los une con comas (Ej: "Boxeo, Pesas")
        else:
            return "⛔ Sin Membresía" # Si no pagó o venció
    
    ver_disciplinas_activas.short_description = "Entrena (Activo)"

# 2. Configuración para Pagos
class PagoAdmin(admin.ModelAdmin):
    list_display = ('alumno', 'monto', 'fecha_pago', 'fecha_vencimiento', 'mostrar_disciplinas')
    list_filter = ('fecha_pago', 'disciplinas') 
    search_fields = ('alumno__nombre', 'alumno__apellido', 'alumno__dni')
    
    filter_horizontal = ('disciplinas',) 

    def mostrar_disciplinas(self, obj):
        return ", ".join([d.nombre for d in obj.disciplinas.all()])
    mostrar_disciplinas.short_description = "Deportes Pagados"

    # --- AQUÍ ESTÁ LA SOLUCIÓN ---
    # Esto inyecta el CSS de corrección solo en la pantalla de Pagos
    class Media:
        css = {
            'all': ('asistencia/parche_cajas.css',)
        }

# 3. Registramos todo
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Asistencia)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Disciplina)