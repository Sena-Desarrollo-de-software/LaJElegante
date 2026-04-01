from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
import csv
import pandas as pd
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponse
from .models import Habitacion, TipoHabitacion, ReservaHabitacion
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm, HabitacionRestoreForm
from core.utils import ahora

HABITACION_INDEX = "rooms:habitacion_index"

# === HABITACIÓN ===
def filtrar_habitaciones(request, queryset=None):
    if queryset is None:
        queryset = Habitacion.objects.all()
    
    tipo = request.GET.get("tipo")
    estado = request.GET.get("estado")
    numero = request.GET.get("numero")

    if tipo:
        queryset = queryset.filter(tipo_habitacion_id=tipo)

    if estado:
        queryset = queryset.filter(estado=estado)

    if numero:
        queryset = queryset.filter(numero_habitacion=numero)

    return queryset

def generar_pdf_habitaciones(habitaciones, filtros, request):

    context = {
        'habitaciones' : habitaciones,
        'filtros' : filtros,
        'total_registros' : habitaciones.count(),
        'usuario' : request.user,
        'fecha_exportacion' : ahora(),
        'tipos' : TipoHabitacion.objects.all(),
    }

    html_string = render_to_string('backoffice/habitaciones/habitacion_pdf.html', context)
    pdf = HTML(string=html_string).write_pdf()

    return pdf

@login_required
@permission_required("rooms.add_habitacion", raise_exception=True)
def descargar_plantilla_habitaciones(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plantilla_habitaciones.csv"'
    
    writer = csv.writer(response)
    
    writer.writerow([
        'numero_habitacion',
        'tipo_habitacion',
        'estado',
    ])
    
    tipos = TipoHabitacion.objects.filter(is_active=True)
    
    writer.writerow(['# INSTRUCCIONES:'])
    writer.writerow(['# - numero_habitacion: Número único de la habitación (obligatorio)'])
    writer.writerow(['# - tipo_habitacion: Debe coincidir exactamente con los nombres del sistema'])
    writer.writerow(['# - estado: DISPONIBLE, OCUPADA, RESERVADA o MANTENIMIENTO (opcional)'])
    writer.writerow(['#'])
    writer.writerow(['# Tipos de habitación disponibles:'])
    for tipo in tipos:
        writer.writerow([f'#   - {tipo.get_nombre_tipo_display()}'])
    writer.writerow(['#'])
    writer.writerow(['# EJEMPLOS:'])
    
    if tipos.exists():
        writer.writerow(['101', tipos[0].get_nombre_tipo_display(), 'DISPONIBLE'])
        writer.writerow(['102', tipos[0].get_nombre_tipo_display(), 'OCUPADA'])
        if tipos.count() > 1:
            writer.writerow(['201', tipos[1].get_nombre_tipo_display(), 'RESERVADA'])
    else:
        writer.writerow(['101', 'Basica', 'DISPONIBLE'])
        writer.writerow(['102', 'Basica', 'OCUPADA'])
    
    writer.writerow(['#'])
    writer.writerow(['# Borrar esta línea y empezar a agregar tus datos:'])
    
    return response

@login_required
@permission_required("rooms.view_habitacion", raise_exception=True)
@require_safe
def index_habitacion(request):
    habitaciones = filtrar_habitaciones(request)

    tipos = TipoHabitacion.objects.all()

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_habitaciones(habitaciones, request.GET, request)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"habitaciones_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render(request, "backoffice/habitaciones/habitacion_index.html", {
        "habitaciones": habitaciones,
        "tipos": tipos,
        "filtros": request.GET
    })

@login_required
@permission_required("rooms.add_habitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_habitacion(request):
    form = HabitacionCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        habitacion = form.save(commit=False)
        habitacion.created_by = request.user
        habitacion.updated_by = request.user
        habitacion.save()

        return redirect(HABITACION_INDEX)

    return render(request, "backoffice/habitaciones/habitacion_create.html", {
        "form": form
    })

@login_required
@permission_required("rooms.change_habitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion.objects, pk=pk)
    form = HabitacionUpdateForm(request.POST or None, instance=habitacion)

    if form.is_valid():
        habitacion = form.save(commit=False)
        habitacion.updated_by = request.user
        habitacion.save()

        return redirect(HABITACION_INDEX)

    return render(request, "backoffice/habitaciones/habitacion_update.html", {
        "form": form,
        "habitacion": habitacion
    })

@login_required
@permission_required("rooms.delete_habitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion.objects, pk=pk)
    form = HabitacionDeleteForm(request.POST or None, habitacion=habitacion)

    if form.is_valid():
        habitacion.soft_delete(user=request.user)
        return redirect(HABITACION_INDEX)

    return render(request, "backoffice/habitaciones/habitacion_delete.html", {
        "form": form,
        "habitacion": habitacion
    })

@login_required
@permission_required("rooms.delete_habitacion", raise_exception=True)
@require_safe
def trashcan_habitacion(request):
    habitaciones = Habitacion.all_objects.filter(is_active=False)

    return render(request, "backoffice/habitaciones/habitacion_trashcan.html", {
        "habitaciones": habitaciones
    })

@login_required
@permission_required("rooms.change_habitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_habitacion(request, pk):
    habitacion = get_object_or_404(
        Habitacion.all_objects,
        pk=pk,
        is_active=False
    )

    form = HabitacionRestoreForm(
        request.POST or None,
        habitacion=habitacion
    )

    if form.is_valid():
        habitacion.restore(user=request.user)
        return redirect("rooms:habitacion_trashcan")

    return render(request, "backoffice/habitaciones/habitacion_restore.html", {
        "form": form,
        "habitacion": habitacion
    })

@login_required
@permission_required("rooms.add_habitacion", raise_exception=True)
def import_habitacion(request):
    context = {
        'title': 'Importar Habitaciones',
        'subtitle': 'Carga masiva de habitaciones desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
    }
    return render(request, 'backoffice/habitaciones/habitacion_import.html', context)

# rooms/views.py - Actualiza la parte de procesamiento

@login_required
@permission_required("rooms.add_habitacion", raise_exception=True)
def procesar_import_habitacion(request):
    """Procesa el archivo subido y realiza la importación"""
    
    if request.method != 'POST':
        return redirect('rooms:habitacion_import')
    
    archivo = request.FILES.get('archivo')
    if not archivo:
        messages.error(request, "No se ha seleccionado ningún archivo")
        return redirect('rooms:habitacion_import')
    
    # Opciones de importación
    actualizar_existentes = request.POST.get('actualizar_existentes') == 'on'
    
    resultados = {
        'creadas': 0,
        'actualizadas': 0,
        'errores': [],
        'tipos_invalidos': [],  # Tipos que no coinciden
    }
    
    try:
        # Leer archivo
        if archivo.name.endswith('.csv'):
            archivo.seek(0)
            try:
                df = pd.read_csv(archivo, encoding='utf-8')
            except UnicodeDecodeError:
                archivo.seek(0)
                df = pd.read_csv(archivo, encoding='latin-1')
        else:
            archivo.seek(0)
            df = pd.read_excel(archivo)
        
        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Validar columnas requeridas
        columnas_requeridas = ['numero_habitacion', 'tipo_habitacion']
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        
        if columnas_faltantes:
            messages.error(request, 
                f'Columnas requeridas faltantes: {", ".join(columnas_faltantes)}. '
                f'Columnas encontradas: {", ".join(list(df.columns))}')
            return redirect('rooms:habitacion_import')
        
        # Obtener tipo por defecto (BASICA)
        try:
            tipo_por_defecto = TipoHabitacion.objects.get(nombre_tipo='BASICA')
        except TipoHabitacion.DoesNotExist:
            messages.error(request, "El tipo de habitación 'BASICA' no existe. Por favor, créalo primero en el sistema.")
            return redirect('rooms:habitacion_import')
        
        # Mapeo de nombres de tipos (para manejar variaciones)
        mapeo_tipos = {
            'familiar': 'FAMILIAR',
            'pareja': 'PAREJA', 
            'basica': 'BASICA',
            'básica': 'BASICA',
            'especial': 'ESPECIAL',
            'simple': 'BASICA',
            'doble': 'PAREJA',
            'matrimonial': 'PAREJA',
            'suite': 'ESPECIAL',
        }
        
        with transaction.atomic():
            for idx, row in df.iterrows():
                try:
                    numero = str(row['numero_habitacion']).strip()
                    tipo_input = str(row['tipo_habitacion']).strip().lower()
                    estado = str(row.get('estado', 'DISPONIBLE')).strip() if 'estado' in df.columns else 'DISPONIBLE'
                    
                    if not numero:
                        resultados['errores'].append(f"Fila {idx+2}: Número de habitación vacío")
                        continue
                    
                    # Validar tipo de habitación
                    tipo = None
                    tipo_normalizado = mapeo_tipos.get(tipo_input, tipo_input.upper())
                    
                    try:
                        # Buscar el tipo exacto
                        tipo = TipoHabitacion.objects.get(nombre_tipo=tipo_normalizado)
                    except TipoHabitacion.DoesNotExist:
                        # Si no existe, buscar por display name
                        try:
                            tipo = TipoHabitacion.objects.filter(
                                nombre_tipo__in=[choice[0] for choice in TipoHabitacion.NOMBRE_TIPO_CHOICES]
                            ).filter(
                                models.Q(nombre_tipo=tipo_normalizado) |
                                models.Q(nombre_tipo__iexact=tipo_input) |
                                models.Q(descripcion__iexact=tipo_input)
                            ).first()
                        except:
                            pass
                        
                        if not tipo:
                            # Usar tipo por defecto
                            tipo = tipo_por_defecto
                            resultados['tipos_invalidos'].append(f"Fila {idx+2}: '{tipo_input}' → asignado a 'BASICA'")
                    
                    # Validar estado
                    if estado not in ['DISPONIBLE', 'OCUPADA', 'RESERVADA', 'MANTENIMIENTO']:
                        estado = 'DISPONIBLE'
                    
                    # Buscar o crear habitación
                    habitacion, created = Habitacion.objects.get_or_create(
                        numero_habitacion=numero,
                        defaults={
                            'tipo_habitacion': tipo,
                            'estado': estado,
                            'is_active': True,
                        }
                    )
                    
                    if not created:
                        if actualizar_existentes:
                            habitacion.tipo_habitacion = tipo
                            habitacion.estado = estado
                            habitacion.save()
                            resultados['actualizadas'] += 1
                        else:
                            resultados['errores'].append(f"Fila {idx+2}: Habitación {numero} ya existe")
                    else:
                        resultados['creadas'] += 1
                        
                except Exception as e:
                    resultados['errores'].append(f"Fila {idx+2}: {str(e)}")
        
        # Mensajes de resultado
        if resultados['creadas'] > 0:
            messages.success(request, f"{resultados['creadas']} habitaciones creadas")
        if resultados['actualizadas'] > 0:
            messages.info(request, f"{resultados['actualizadas']} habitaciones actualizadas")
        if resultados['tipos_invalidos']:
            messages.warning(request, 
                f"⚠️ Tipos no válidos: {len(resultados['tipos_invalidos'])} fueron asignados a 'BASICA'. "
                f"Detalles: {'; '.join(resultados['tipos_invalidos'][:3])}")
        if resultados['errores']:
            messages.error(request, f"{len(resultados['errores'])} errores: {'; '.join(resultados['errores'][:3])}")
            request.session['import_errores'] = resultados['errores']
            
    except Exception as e:
        messages.error(request, f"Error al procesar archivo: {str(e)}")
        import traceback
        traceback.print_exc()
    
    return redirect('rooms:habitacion_index')

# === RESERVA HABITACION ===
@require_GET
def index_reserva_habitacion(request):
    return render(request,'backoffice/reserva_habitaciones/reserva_habitacion_index.html')

@require_POST
def create_reserva_habitacion(request):
    return render(request,'backoffice/reserva_habitaciones/reserva_habitacion_create.html')

@require_http_methods(['POST','GET'])
def update_reserva_habitacion(request):
    return render(request,'backoffice/reserva_habitaciones/reserva_habitacion_update.html')

@require_http_methods(['POST','GET'])
def delete_reserva_habitacion(request):
    return render(request, 'backoffice/reserva_habitaciones/reserva_habitacion_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_reserva_habitacion(request):
    return render(request,'backoffice/reserva_habitaciones/reserva_habitacion_trashcan.html')

# === TIPO HABITACION ===
@require_GET
def index_tipo_habitacion(request):
    return render(request,'backoffice/tipo_habitacion/tipo_habitacion_index.html')

@require_POST
def create_tipo_habitacion(request):
    return render(request,'backoffice/tipo_habitacion/tipo_habitacion_create.html')

@require_http_methods(['POST','GET'])
def update_tipo_habitacion(request):
    return render(request,'backoffice/tipo_habitacion/tipo_habitacion_update.html')

@require_http_methods(['POST','GET'])
def delete_tipo_habitacion(request):
    return render(request, 'backoffice/tipo_habitacion/tipo_habitacion_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_tipo_habitacion(request):
    return render(request,'backoffice/tipo_habitacion/tipo_habitacion_trashcan.html')