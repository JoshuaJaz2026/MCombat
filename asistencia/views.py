from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from datetime import timedelta
import json
import openpyxl

from .models import Alumno, Asistencia, Pago

# ========================================================
# 1. REGISTRO DE ASISTENCIA (EL CADENERO)
# ========================================================
@login_required(login_url='login_asistencia')
def registro_asistencia(request):
    context = {}

    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        
        try:
            alumno_encontrado = Alumno.objects.get(dni=dni_ingresado)
            
            # Verificamos si está al día
            if alumno_encontrado.esta_al_dia():
                Asistencia.objects.create(alumno=alumno_encontrado)
                context = {
                    'alumno': alumno_encontrado,
                    'estado': 'exito',
                    'mensaje': f"¡Bienvenido, {alumno_encontrado.nombre}!",
                    'submensaje': f"Vencimiento: {alumno_encontrado.fecha_vencimiento}"
                }
            else:
                context = {
                    'alumno': alumno_encontrado,
                    'estado': 'error',
                    'mensaje': "⛔ ACCESO DENEGADO",
                    'submensaje': f"Tu membresía venció el {alumno_encontrado.fecha_vencimiento}. Por favor pasa por caja."
                }

        except Alumno.DoesNotExist:
            messages.error(request, "❌ DNI no encontrado en el sistema.")

    return render(request, 'registro.html', context)

# ========================================================
# 2. EXPORTAR EXCEL
# ========================================================
@login_required(login_url='login_asistencia')
def exportar_alumnos_excel(request):
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Alumnos MCombat'

    headers = ['ID', 'Nombre', 'Apellido', 'DNI', 'Fecha Registro']
    worksheet.append(headers)

    alumnos = Alumno.objects.all()

    for alumno in alumnos:
        fecha_reg = str(alumno.fecha_registro.date()) if alumno.fecha_registro else '-'
        worksheet.append([alumno.id, alumno.nombre, alumno.apellido, alumno.dni, fecha_reg])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_alumnos.xlsx"'
    workbook.save(response)
    return response

# ========================================================
# 3. DASHBOARD (CORREGIDO)
# ========================================================
@staff_member_required
def dashboard_view(request):
    # A. TARJETAS
    total_alumnos = Alumno.objects.count()
    hoy = timezone.now().date()
    asistencias_hoy = Asistencia.objects.filter(fecha__date=hoy).count()
    
    mes_actual = hoy.month
    ingresos_mes = Pago.objects.filter(fecha_pago__month=mes_actual).aggregate(Sum('monto'))['monto__sum']
    if ingresos_mes is None:
        ingresos_mes = 0

    # B. GRÁFICO (Aquí estaba el error)
    labels = []
    data = []
    
    for i in range(6, -1, -1):
        fecha_analisis = hoy - timedelta(days=i)
        
        # --- CORRECCIÓN ---
        # Buscamos en el campo 'fecha' (que es el de la BD), comparándolo con la variable 'fecha_analisis'
        cnt = Asistencia.objects.filter(fecha__date=fecha_analisis).count()

        labels.append(fecha_analisis.strftime("%d/%m"))
        data.append(cnt)

    context = {
        'total_alumnos': total_alumnos,
        'asistencias_hoy': asistencias_hoy,
        'ingresos_mes': ingresos_mes,
        'chart_labels': json.dumps(labels),
        'chart_data': json.dumps(data),
    }
    
    return render(request, 'admin/dashboard.html', context)
# asistencia/views.py
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Esta vista funciona como un "Semáforo"
@login_required
def smart_login_redirect(request):
    # Si es Superusuario (Dueño), lo mandamos al Admin Panel (Jazzmin)
    if request.user.is_superuser:
        return redirect('/admin/')
    
    # Para todos los demás (Staff/Alumnos), los mandamos a su Dashboard
    else:
        return redirect('/admin/dashboard/')