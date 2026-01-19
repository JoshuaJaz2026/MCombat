from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout as django_logout
from django.db.models import Sum
from datetime import timedelta
import json
import openpyxl

from .models import Alumno, Asistencia, Pago

# ========================================================
# 1. SEMÁFORO INTELIGENTE (Detecta si es Jefe o Staff)
# ========================================================
@login_required
def smart_login_redirect(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('dashboard')

# ========================================================
# 2. LOGOUT (Cerrar Sesión)
# ========================================================
def logout(request):
    django_logout(request)
    return redirect('login_asistencia') 

# ========================================================
# 3. DASHBOARD (Zona Staff)
# ========================================================
@staff_member_required
def dashboard(request):
    # A. TARJETAS DE DATOS
    total_alumnos = Alumno.objects.count()
    hoy = timezone.now().date()
    asistencias_hoy = Asistencia.objects.filter(fecha__date=hoy).count()
    
    mes_actual = hoy.month
    ingresos_mes = Pago.objects.filter(fecha_pago__month=mes_actual).aggregate(Sum('monto'))['monto__sum']
    if ingresos_mes is None:
        ingresos_mes = 0

    # B. GRÁFICO DE BARRAS
    labels = []
    data = []
    for i in range(6, -1, -1):
        fecha_analisis = hoy - timedelta(days=i)
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
    
    # Renderiza la plantilla que está en la carpeta admin
    return render(request, 'admin/dashboard.html', context)

# ========================================================
# 4. REGISTRO DE ASISTENCIA (Para el Profesor)
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
                    'submensaje': f"Membresía vencida el {alumno_encontrado.fecha_vencimiento}"
                }

        except Alumno.DoesNotExist:
            messages.error(request, "❌ DNI no encontrado.")

    # Renderiza la plantilla que está suelta en templates
    return render(request, 'registro.html', context)

# ========================================================
# 5. EXPORTAR EXCEL
# ========================================================
@login_required(login_url='login_asistencia')
def exportar_excel(request):
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