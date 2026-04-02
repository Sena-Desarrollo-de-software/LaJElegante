from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from weasyprint import HTML
import csv
from django.http import HttpResponse
from .models import Habitacion, TipoHabitacion, ReservaHabitacion
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm, HabitacionRestoreForm
from .importers import HabitacionImporter
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
    tipos = TipoHabitacion.objects.filter(is_active=True)
    estados = Habitacion.ESTADO_HABITACION_CHOICES  
    context = {
        'title': 'Importar Habitaciones',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
        'tipos' : tipos,
        'estados' : estados
    }
    return render(request, 'backoffice/habitaciones/habitacion_import.html', context)

@login_required
@permission_required("rooms.add_habitacion", raise_exception=True)
def procesar_import_habitacion(request):
    if request.method != 'POST':
        return redirect('rooms:habitacion_import')
    archivo = request.FILES.get('archivo')
    actualizar = request.POST.get('actualizar_existentes') == 'on'
    importer = HabitacionImporter(request, update_existing=actualizar)
    importer.run(archivo)
    importer.add_messages()
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