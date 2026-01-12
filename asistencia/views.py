from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
# --- IMPORTES PARA EL DASHBOARD ---
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from datetime import timedelta
import json
import openpyxl

# Importamos tus modelos
from .models import Alumno, Asistencia, Pago

# ========================================================
# 1. VISTA DE REGISTRO DE ASISTENCIA
# ========================================================
# asistencia/views.py

@login_required(login_url='login_asistencia')
def registro_asistencia(request):
    # Variables para enviar a la plantilla (por defecto vacías)
    context = {}

    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        
        try:
            alumno_encontrado = Alumno.objects.get(dni=dni_ingresado)
            hoy = timezone.now().date()
            
            # Buscamos pago válido
            pago_activo = Pago.objects.filter(
                alumno=alumno_encontrado, 
                fecha_vencimiento__gte=hoy
            ).order_by('-fecha_vencimiento').first()

            if pago_activo:
                Asistencia.objects.create(alumno=alumno_encontrado)
                
                # ✅ ÉXITO: Enviamos los datos del alumno y el pago al HTML
                context = {
                    'alumno': alumno_encontrado,
                    'pago': pago_activo,
                    'estado': 'exito', # Para pintar verde
                    'mensaje': f"¡Bienvenido, {alumno_encontrado.nombre}!"
                }
            else:
                # ⛔ MOROSO: Enviamos datos pero con estado de error
                context = {
                    'alumno': alumno_encontrado,
                    'estado': 'error', # Para pintar rojo
                    'mensaje': f"⛔ ALTO {alumno_encontrado.nombre}. Membresía vencida."
                }

        except Alumno.DoesNotExist:
            messages.error(request, "❌ DNI no encontrado en el sistema.")
            return redirect('registro_asistencia')

    return render(request, 'registro.html', context)


# ========================================================
# 2. VISTA PARA EXPORTAR EXCEL
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
        
        worksheet.append([
            alumno.id,
            alumno.nombre,
            alumno.apellido,
            alumno.dni,
            fecha_reg
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_alumnos.xlsx"'
    
    workbook.save(response)
    return response


# ========================================================
# 3. VISTA DEL DASHBOARD
# ========================================================
@staff_member_required
def dashboard_view(request):
    # --- A. TARJETAS (KPIs) ---
    total_alumnos = Alumno.objects.count()
    
    hoy = timezone.now().date()
    asistencias_hoy = Asistencia.objects.filter(fecha__date=hoy).count()
    
    mes_actual = hoy.month
    ingresos_mes = Pago.objects.filter(fecha_pago__month=mes_actual).aggregate(Sum('monto'))['monto__sum']
    
    if ingresos_mes is None:
        ingresos_mes = 0

    # --- B. DATOS GRÁFICO (Últimos 7 días) ---
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
    
    return render(request, 'admin/dashboard.html', context)