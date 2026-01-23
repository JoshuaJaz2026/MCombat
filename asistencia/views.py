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

# Importamos tus modelos
from .models import Alumno, Asistencia, Pago

# ========================================================
# 1. SEMÁFORO INTELIGENTE (Detecta si es Jefe o Staff)
# ========================================================
@login_required
def smart_login_redirect(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        # Redirige al dashboard personalizado
        return redirect('dashboard')

# ========================================================
# 2. LOGOUT (Cerrar Sesión)
# ========================================================
def logout(request):
    django_logout(request)
    return redirect('login_asistencia') 

# ========================================================
# 3. DASHBOARD (Panel de Estadísticas)
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

    # B. GRÁFICO DE BARRAS (Últimos 7 días)
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
    
    # Renderiza la plantilla del dashboard
    return render(request, 'admin/dashboard.html', context)

# ========================================================
# 4. REGISTRO DE ASISTENCIA (Para el Profesor/Tablet)
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

    return render(request, 'registro.html', context)

# ========================================================
# 5. EXPORTAR EXCEL (Asistencias)
# ========================================================
@staff_member_required
def exportar_asistencias_excel(request):
    # 1. Configurar el tipo de archivo (Excel)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte_Asistencias_MCombat.xlsx'

    # 2. Crear el libro de Excel y la hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Asistencias"

    # 3. Encabezados
    columns = ['Fecha', 'Alumno', 'Hora', 'Día']
    ws.append(columns)

    # 4. Obtener datos
    rows = Asistencia.objects.all().order_by('-fecha', '-hora')

    # 5. Escribir filas
    for row in rows:
        ws.append([
            row.fecha.strftime("%Y-%m-%d"), # Fecha limpia
            str(row.alumno),                # CORREGIDO: Usamos 'alumno' en lugar de 'usuario'
            row.hora.strftime("%H:%M"),     # Hora limpia
            row.fecha.strftime("%A")        # Día de la semana
        ])

    # 6. Guardar y enviar
    wb.save(response)
    return response

# Si necesitas exportar la lista de alumnos (opcional, lo dejo por si acaso)
@staff_member_required
def exportar_alumnos_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Alumnos MCombat'
    headers = ['ID', 'Nombre', 'Apellido', 'DNI', 'Fecha Registro']
    ws.append(headers)
    alumnos = Alumno.objects.all()
    for alumno in alumnos:
        fecha_reg = str(alumno.fecha_registro.date()) if alumno.fecha_registro else '-'
        ws.append([alumno.id, alumno.nombre, alumno.apellido, alumno.dni, fecha_reg])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Listado_Alumnos.xlsx"'
    wb.save(response)
    return response