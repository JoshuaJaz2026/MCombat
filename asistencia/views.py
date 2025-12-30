from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Alumno, Asistencia, Pago
from django.utils import timezone

def registro_asistencia(request):
    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        
        try:
            # 1. Buscamos al alumno
            alumno_encontrado = Alumno.objects.get(dni=dni_ingresado)
            hoy = timezone.now().date()

            # 2. Buscamos si tiene algún pago válido (que venza hoy o en el futuro)
            pago_activo = Pago.objects.filter(
                alumno=alumno_encontrado, 
                fecha_vencimiento__gte=hoy
            ).order_by('-fecha_vencimiento').first()

            if pago_activo:
                # ✅ TIENE PAGO AL DÍA -> Pasa y se registra asistencia
                Asistencia.objects.create(alumno=alumno_encontrado)
                messages.success(request, f"¡Bienvenido, {alumno_encontrado.nombre}! 🥊 (Vence: {pago_activo.fecha_vencimiento})")
            else:
                # ⛔ NO PAGÓ O VENCIÓ -> Bloqueo total
                messages.error(request, f"⛔ ALTO {alumno_encontrado.nombre}. Tu membresía ha vencido o no tienes pagos.")

        except Alumno.DoesNotExist:
            # ❌ DNI NO EXISTE
            messages.error(request, "❌ DNI no encontrado en el sistema.")
        
        return redirect('registro_asistencia')

    return render(request, 'registro.html')