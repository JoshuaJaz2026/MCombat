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
# 1. VISTA DE REGISTRO DE ASISTENCIA (EL CADENERO) 🛡️
# ========================================================
@login_required(login_url='login_asistencia')
def registro_asistencia(request):
    context = {} # Variables vacías al inicio

    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        
        try:
            # 1. Buscamos al alumno por DNI
            alumno_encontrado = Alumno.objects.get(dni=dni_ingresado)
            
            # 2. EL CADENERO: Preguntamos si está al día
            # Usamos la función inteligente que creamos en models.py
            if alumno_encontrado.esta_al_dia():
                
                # --- ✅ LUZ VERDE: ACCESO PERMITIDO ---
                Asistencia.objects.create(alumno=alumno_encontrado)
                
                context = {
                    'alumno': alumno_encontrado,
                    'estado': 'exito', # Esto activa el CSS VERDE
                    'mensaje': f"¡Bienvenido, {alumno_encontrado.nombre}!",
                    'submensaje': f"Vencimiento: {alumno_encontrado.fecha_vencimiento}"
                }
            
            else:
                # --- ❌ LUZ ROJA: ACCESO DENEGADO ---
                # NO registramos asistencia. Lo rebotamos en la puerta.
                context = {
                    'alumno': alumno_encontrado,
                    'estado': 'error', # Esto activa el CSS ROJO
                    'mensaje': "⛔ ACCESO DENEGADO",
                    'submensaje': f"Tu membresía venció el {alumno_encontrado.fecha_vencimiento}. Por favor pasa por caja."
                }

        except Alumno.DoesNotExist:
            # Si el DNI no existe
            messages.error(request, "❌ DNI no encontrado en el sistema.")
            # No hacemos redirect para que se muestre el mensaje en la misma pantalla

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
        cnt = Asistencia.objects.filter(fecha_analisis__date=fecha_analisis).count() # Corrección pequeña aquí
        # Si da error usa: filter(fecha__date=fecha_analisis) dependiendo de tu base de datos
        # Vamos a dejarlo estándar:
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