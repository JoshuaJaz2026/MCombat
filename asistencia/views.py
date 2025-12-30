from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Alumno, Asistencia, Pago
from django.utils import timezone
import openpyxl
from django.http import HttpResponse

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

def exportar_alumnos_excel(request):
    # 1. Crear el libro de Excel (el archivo)
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Alumnos MCombat'

    # 2. Crear los encabezados (la primera fila en negrita)
    headers = ['ID', 'Nombre', 'Apellido', 'DNI', 'Fecha Registro']
    worksheet.append(headers)

    # 3. Sacar los datos de la base de datos
    # (Asegúrate de que tu modelo se llame 'Alumno', si no, cámbialo aquí)
    alumnos = Alumno.objects.all()

    # 4. Escribir fila por fila
    for alumno in alumnos:
        # Ajusta estos campos según cómo se llamen en tu models.py
        worksheet.append([
            alumno.id,
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            str(alumno.fecha_registro) # Convertimos fecha a texto
        ])

    # 5. Preparar la respuesta para descargar
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_alumnos.xlsx"'
    
    workbook.save(response)
    return response