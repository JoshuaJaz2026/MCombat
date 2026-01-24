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

# --- IMPORTANTE: Herramientas de diseño para Excel ---
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Importamos tus modelos
from .models import Alumno, Asistencia, Pago

# ========================================================
# 1. SEMÁFORO INTELIGENTE
# ========================================================
@login_required
def smart_login_redirect(request):
    if request.user.is_superuser:
        return redirect('/admin/')
    else:
        return redirect('dashboard')

# ========================================================
# 2. LOGOUT
# ========================================================
def logout(request):
    django_logout(request)
    return redirect('login_asistencia') 

# ========================================================
# 3. DASHBOARD
# ========================================================
@staff_member_required
def dashboard(request):
    total_alumnos = Alumno.objects.count()
    hoy = timezone.now().date()
    asistencias_hoy = Asistencia.objects.filter(fecha__date=hoy).count()
    
    mes_actual = hoy.month
    ingresos_mes = Pago.objects.filter(fecha_pago__month=mes_actual).aggregate(Sum('monto'))['monto__sum']
    if ingresos_mes is None:
        ingresos_mes = 0

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

# ========================================================
# 4. REGISTRO DE ASISTENCIA
# ========================================================
@login_required(login_url='login_asistencia')
def registro_asistencia(request):
    context = {}
    if request.method == 'POST':
        dni_ingresado = request.POST.get('dni')
        try:
            alumno_encontrado = Alumno.objects.get(dni=dni_ingresado)
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
# 5. EXPORTAR EXCEL (DISEÑO PRO MCOMBAT)
# ========================================================
@staff_member_required
def exportar_asistencias_excel(request):
    # 1. Configurar respuesta HTTP
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=Reporte_Asistencias_MCombat.xlsx'

    # 2. Crear libro y hoja
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Historial Asistencias"

    # --- DEFINIR ESTILOS ---
    # Rojo MCombat para fondo
    header_fill = PatternFill(start_color='E50914', end_color='E50914', fill_type='solid')
    # Texto Blanco y Negrita
    header_font = Font(name='Arial', size=12, bold=True, color='FFFFFF')
    # Alineación centrada
    center_align = Alignment(horizontal='center', vertical='center')
    # Bordes finos
    thin_border = Border(left=Side(style='thin'), right=Side(style='thin'), 
                         top=Side(style='thin'), bottom=Side(style='thin'))

    # 3. Encabezados
    columns = ['FECHA', 'ALUMNO', 'HORA', 'DÍA']
    
    # Escribir y estilizar encabezados (Fila 1)
    for col_num, column_title in enumerate(columns, 1):
        cell = ws.cell(row=1, column=col_num)
        cell.value = column_title
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align
        cell.border = thin_border

    # 4. Obtener datos
    rows = Asistencia.objects.all().order_by('-id')

    # 5. Escribir datos con estilo (Desde Fila 2)
    for row_num, row in enumerate(rows, 2):
        try:
            hora_formateada = row.fecha.strftime("%H:%M")
        except:
            hora_formateada = "00:00"

        # Datos a escribir
        valores = [
            row.fecha.strftime("%Y-%m-%d"),
            str(row.alumno),
            hora_formateada,
            row.fecha.strftime("%A")
        ]

        # Escribir celda por celda para ponerle borde y alineación
        for col_num, valor in enumerate(valores, 1):
            cell = ws.cell(row=row_num, column=col_num)
            cell.value = valor
            cell.alignment = center_align # Centramos todo el contenido
            cell.border = thin_border     # Ponemos bordes a todo

    # 6. AUTO-AJUSTAR ANCHO DE COLUMNAS
    # Esto recorre las columnas y las ensancha si el texto es largo
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter # Ej: 'A', 'B'
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = (max_length + 2)
        ws.column_dimensions[column].width = adjusted_width

    # 7. Guardar
    wb.save(response)
    return response

# Exportar lista de alumnos (Opcional)
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