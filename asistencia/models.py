from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.html import mark_safe 

# ================================================================
# 1. MODELO DISCIPLINA
# ================================================================
class Disciplina(models.Model):
    nombre = models.CharField(max_length=50, unique=True) # Ej: MMA, Boxeo, Muay Thai
    
    def __str__(self):
        return self.nombre

# ================================================================
# 2. MODELO ALUMNO
# ================================================================
class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI / Identificación")
    
    # --- CAMPO TELEFONO (ACTUALIZADO PARA WHATSAPP) ---
    telefono = models.CharField(max_length=20, blank=True, null=True, verbose_name="Teléfono")
    
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Campo de Foto
    foto = models.ImageField(upload_to='fotos_alumnos/', null=True, blank=True, verbose_name="Foto del Alumno")

    # --- CAMPO CRÍTICO PARA EL CADENERO ---
    fecha_vencimiento = models.DateField(null=True, blank=True, verbose_name="Vencimiento Membresía")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"

    # --- VISUALIZACIÓN DE FOTO EN EL ADMIN ---
    def vista_foto(self):
        if self.foto:
            return mark_safe(f'<img src="{self.foto.url}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />')
        return "Sin foto"
    vista_foto.short_description = "Avatar"

    # --- LÓGICA DEL SEMÁFORO (¿Está al día?) ---
    def esta_al_dia(self):
        """Retorna True si la fecha de vencimiento es hoy o futura."""
        if not self.fecha_vencimiento:
            return False 
        return self.fecha_vencimiento >= timezone.now().date()

# ================================================================
# 3. MODELO ASISTENCIA
# ================================================================
class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asistencia de {self.alumno}"

# ================================================================
# 4. MODELO PAGO
# ================================================================
class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    disciplinas = models.ManyToManyField(Disciplina, verbose_name="Disciplinas Inscritas")
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    
    # Fecha editable, por defecto es hoy
    fecha_pago = models.DateField(default=timezone.now, verbose_name="Fecha de Pago")
    
    fecha_vencimiento = models.DateField(blank=True, null=True) 
    
    def save(self, *args, **kwargs):
        # 1. Si no ponen fecha de vencimiento, calculamos 30 días automáticamente
        if not self.fecha_vencimiento:
            # Usamos la fecha_pago real para calcular el vencimiento
            # (Si fecha_pago viene como datetime, lo convertimos a date)
            fecha_base = self.fecha_pago
            if isinstance(fecha_base, models.DateTimeField): 
                 fecha_base = fecha_base.date()
            elif hasattr(fecha_base, 'date'): # Por seguridad si es un objeto timezone
                 fecha_base = fecha_base.date()
            
            self.fecha_vencimiento = fecha_base + timedelta(days=30)
        
        # 2. Guardamos el Pago
        super().save(*args, **kwargs)

        # 3. Actualizamos al Alumno Automáticamente
        self.alumno.fecha_vencimiento = self.fecha_vencimiento
        self.alumno.save()

    def __str__(self):
        return f"Pago de {self.alumno} (Vence: {self.fecha_vencimiento})"