from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.utils.html import format_html # Importante para el botón de WhatsApp
from .models import Alumno, Asistencia, Pago, Disciplina

# ================================================================
# 1. PERSONALIZACIÓN DE USUARIOS (ROLES VISUALES)
# ================================================================

# Primero: "Des-registramos" el admin de usuarios por defecto
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass

# Segundo: Registramos nuestro admin personalizado con la columna ROL
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Agregamos 'ver_rol' a las columnas visibles
    list_display = ('username', 'email', 'first_name', 'last_name', 'ver_rol', 'is_active')
    
    # Filtros laterales
    list_filter = ('is_superuser', 'is_staff', 'is_active')

    # --- LÓGICA DE LA COLUMNA DE ROLES ---
    @admin.display(description='ROL DEL SISTEMA')
    def ver_rol(self, obj):
        if obj.is_superuser:
            # Color Rojo y Corona para el Jefe
            return mark_safe('<span style="color: #d9534f; font-weight: bold; font-size: 1.1em;">👑 ADMINISTRADOR</span>')
        elif obj.is_staff:
            # Color Azul y Guante para el Staff
            return mark_safe('<span style="color: #0275d8; font-weight: bold;">🥊 STAFF</span>')
        else:
            return mark_safe('<span style="color: #777;">👤 USUARIO</span>')

# ================================================================
# 2. CONFIGURACIÓN DE ALUMNOS (CON WHATSAPP)
# ================================================================
class AlumnoAdmin(admin.ModelAdmin):
    # Agregamos 'telefono' y 'boton_whatsapp' a las columnas
    list_display = ('vista_foto', 'nombre', 'apellido', 'dni', 'telefono', 'boton_whatsapp', 'fecha_vencimiento', 'estado_pago')
    
    # Esto hace que la FOTO y el NOMBRE sean clics para editar
    list_display_links = ('vista_foto', 'nombre') 
    
    search_fields = ('nombre', 'apellido', 'dni')
    list_filter = ('fecha_vencimiento',)

    # --- NUEVO: BOTÓN DE WHATSAPP ---
    def boton_whatsapp(self, obj):
        if obj.telefono:
            # Limpiamos el número (quitamos espacios o guiones)
            numero_limpio = str(obj.telefono).replace(" ", "").replace("-", "")
            
            # Link oficial de WhatsApp API (Agregamos 51 de Perú)
            link = f"https://wa.me/51{numero_limpio}"
            
            # Retornamos el botón verde
            return format_html(
                '<a href="{}" target="_blank" style="background-color:#25D366; color:white; padding:4px 10px; border-radius:15px; text-decoration:none; font-weight:bold; font-family:sans-serif; font-size: 12px;">'
                '💬 Chat'
                '</a>',
                link
            )
        else:
            return "-"
    boton_whatsapp.short_description = "WhatsApp"

    # --- SEMÁFORO VISUAL ---
    def estado_pago(self, obj):
        if obj.esta_al_dia():
            return mark_safe('<span style="color: green; font-weight: bold;">✅ Al día</span>')
        return mark_safe('<span style="color: red; font-weight: bold;">❌ Vencido</span>')
    
    estado_pago.short_description = "Estado Membresía"

# ================================================================
# 3. CONFIGURACIÓN DE PAGOS
# ================================================================
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

# ================================================================
# 4. REGISTRO DE MODELOS
# ================================================================
admin.site.register(Alumno, AlumnoAdmin)
admin.site.register(Asistencia)
admin.site.register(Pago, PagoAdmin)
admin.site.register(Disciplina)