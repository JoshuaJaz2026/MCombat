from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.utils.html import mark_safe 

class Disciplina(models.Model):
    nombre = models.CharField(max_length=50, unique=True) # Ej: MMA, Boxeo, Muay Thai
    
    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI / Identificación")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    # Campo de Foto
    foto = models.ImageField(upload_to='fotos_alumnos/', null=True, blank=True, verbose_name="Foto del Alumno")

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.dni})"

    def vista_foto(self):
        if self.foto:
            return mark_safe(f'<img src="{self.foto.url}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />')
        return "Sin foto"
    vista_foto.short_description = "Avatar"

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asistencia de {self.alumno}"

class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    # --- NUEVO: Se puede elegir una o varias disciplinas ---
    disciplinas = models.ManyToManyField(Disciplina, verbose_name="Disciplinas Inscritas")
    
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    fecha_pago = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField(blank=True, null=True) 
    
    def save(self, *args, **kwargs):
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = timezone.now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago de {self.alumno} (Vence: {self.fecha_vencimiento})"