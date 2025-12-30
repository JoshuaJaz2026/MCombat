from datetime import timedelta
from django.db import models

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI / Identificación")
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Asistencia de {self.alumno}"

class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=6, decimal_places=2, default=100.00)
    fecha_pago = models.DateField(auto_now_add=True) # Se pone la fecha de hoy sola
    fecha_vencimiento = models.DateField(blank=True, null=True) # Se calculará sola
    
    def save(self, *args, **kwargs):
        # Si no tiene fecha de vencimiento, le sumamos 30 días a hoy
        if not self.fecha_vencimiento:
            from django.utils import timezone
            self.fecha_vencimiento = timezone.now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Pago de {self.alumno} (Vence: {self.fecha_vencimiento})"