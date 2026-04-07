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
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm, HabitacionRestoreForm, TipoHabitacionCreateForm, TipoHabitacionUpdateForm, TipoHabitacionDeleteForm, TipoHabitacionRestoreForm, ReservaHabitacionCreateForm, ReservaHabitacionUpdateForm
from .importers import HabitacionImporter
from core.utils import ahora
from core.models import Reserva
from django.contrib.contenttypes.models import ContentType
from finance.models import get_tarifa_vigente
from django.core.exceptions import ValidationError
from django.contrib import messages
from datetime import datetime

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
    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

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
def filtrar_reservas_habitacion(request):
    qs = ReservaHabitacion.objects.select_related(
        "reserva",
        "habitacion",
        "reserva__usuario"
    )

    if request.GET.get("habitacion"):
        qs = qs.filter(habitacion_id=request.GET.get("habitacion"))

    if request.GET.get("fecha_inicio"):
        qs = qs.filter(fecha_inicio__gte=request.GET.get("fecha_inicio"))

    if request.GET.get("fecha_fin"):
        qs = qs.filter(fecha_fin__lte=request.GET.get("fecha_fin"))

    if request.GET.get("estado"):
        qs = qs.filter(estado=request.GET.get("estado"))

    return qs

def generar_pdf_reserva_habitacion(reservas, filtros, request):
    total_registros = reservas.count()

    total_ingresos = 0
    total_penalizaciones = 0

    for r in reservas:
        if r.reserva.estado in ["CONFIRMADA", "COMPLETADA"]:
            total_ingresos += r.reserva.total
        elif r.reserva.estado == "CANCELADA":
            penalizacion = getattr(r.reserva, "penalizacion", 0)
            total_penalizaciones += penalizacion

    context = {
        'reservas': reservas,
        'filtros': filtros,

        'total_registros': total_registros,
        'total_ingresos': total_ingresos,
        'total_penalizaciones': total_penalizaciones,

        'usuario': request.user,
        'fecha_exportacion': ahora(),
    }

    html_string = render_to_string(
        'backoffice/reserva_habitaciones/reserva_habitacion_pdf.html',
        context
    )

    pdf = HTML(
        string=html_string,
        base_url=request.build_absolute_uri()
    ).write_pdf()

    return pdf

@login_required
@permission_required("rooms.add_reservahabitacion", raise_exception=True)
def descargar_plantilla_reservas_habitacion(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="plantilla_reservas_habitacion.csv"'

    writer = csv.writer(response)

    writer.writerow([
        'usuario',
        'habitacion',
        'fecha_inicio',
        'fecha_fin',
        'estado',
    ])

    return response

@login_required
@permission_required("rooms.view_reservahabitacion", raise_exception=True)
@require_GET
def index_reserva_habitacion(request):

    reservas = filtrar_reservas_habitacion(request)
    habitaciones = Habitacion.objects.all()

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_reserva_habitacion(
            reservas,
            request.GET,
            request
        )

        response = HttpResponse(pdf, content_type='application/pdf')

        filename = f"reservas_habitacion_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"

        response['Content-Disposition'] = f'inline; filename={filename}'

        return response

    return render(request, "backoffice/reserva_habitaciones/reserva_habitacion_index.html", {
        "reservas": reservas,
        "habitaciones": habitaciones,
        "filtros": request.GET
    })

def parse_date(fecha):
    return datetime.strptime(fecha, "%Y-%m-%d").date() if fecha else None


@login_required
@permission_required("rooms.add_reservahabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_reserva_habitacion(request, reserva_id):
    reserva = get_object_or_404(Reserva, pk=reserva_id)

    fecha_inicio_raw = request.GET.get("fecha_inicio") or request.POST.get("fecha_inicio")
    fecha_fin_raw = request.GET.get("fecha_fin") or request.POST.get("fecha_fin")

    fecha_inicio = parse_date(fecha_inicio_raw)
    fecha_fin = parse_date(fecha_fin_raw)

    form = ReservaHabitacionCreateForm(
        request.POST or None,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin
    )

    if request.method == "POST":
        if form.is_valid():
            reserva_habitacion = form.save(commit=False)
            reserva_habitacion.reserva = reserva
            reserva_habitacion.created_by = request.user
            reserva_habitacion.updated_by = request.user
            reserva_habitacion.save()

            messages.success(
                request,
                f"Habitación asignada correctamente del {fecha_inicio} al {fecha_fin}"
            )

            return redirect("backoffice:reserva_detail", pk=reserva.id)

        else:
            messages.error(
                request,
                "Hubo un error al asignar la habitación. Verifica los datos."
            )

    return render(request, "backoffice/reserva_habitaciones/reserva_habitacion_create.html", {
        "form": form,
        "reserva": reserva,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })

@login_required
@permission_required("rooms.change_reservahabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_reserva_habitacion(request, pk):
    reserva_habitacion = get_object_or_404(ReservaHabitacion, pk=pk, is_active=True)

    if request.method == "POST":
        form = ReservaHabitacionUpdateForm(request.POST, instance=reserva_habitacion)
        if form.is_valid():
            reserva_habitacion = form.save(commit=False)
            reserva_habitacion.updated_by = request.user
            reserva_habitacion.save()
            messages.success(request, "Reserva de habitación actualizada correctamente.")
            return redirect('rooms:reserva_habitacion_index')
        else:
            messages.error(request, "Corrige los errores para continuar.")
    else:
        form = ReservaHabitacionUpdateForm(instance=reserva_habitacion)

    return render(request, "backoffice/reserva_habitaciones/reserva_habitacion_update.html", {
        "form": form,
        "reserva_habitacion": reserva_habitacion
    })

@login_required
@permission_required("rooms.change_reservahabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def cancel_reserva_habitacion(request, pk):
    reserva = get_object_or_404(ReservaHabitacion, pk=pk)

    puede, error = reserva.puede_cancelar()
    if not puede:
        messages.error(request, error)
        return redirect("rooms:reserva_habitacion_index")

    penalizacion = reserva.calcular_penalizacion_preview()
    requiere_confirmacion = penalizacion > 0

    if request.method == "POST":

        if requiere_confirmacion and not request.POST.get("acepta_penalizacion"):
            messages.error(request, "Debes aceptar la penalización para continuar")
            return redirect(request.path)

        try:
            penalizacion_real = reserva.cancelar()

            if penalizacion_real > 0:
                messages.warning(
                    request,
                    f"Reserva cancelada con penalización de ${penalizacion_real}"
                )
            else:
                messages.success(request, "Reserva cancelada exitosamente")

            return redirect("rooms:reserva_habitacion_index")

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect(request.path)

    return render(request, "backoffice/reserva_habitaciones/reserva_habitacion_cancel.html", {
        "reserva": reserva,
        "penalizacion": penalizacion,
        "requiere_confirmacion": requiere_confirmacion
    })

@login_required
@permission_required("rooms.add_reservahabitacion", raise_exception=True)
def import_reserva_habitacion(request):

    estados = ReservaHabitacion.ESTADO_RESERVA_CHOICES

    context = {
        'title': 'Importar Reservas de Habitación',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
        'estados': estados
    }

    return render(
        request,
        'backoffice/reserva_habitaciones/reserva_habitacion_import.html',
        context
    )
# === TIPO HABITACION ===
TIPO_HABITACION_INDEX = "rooms:tipo_habitacion_index"

def generar_pdf_tipo_habitacion(tipos, request):

    context = {
        'tipos': tipos,
        'total_registros': tipos.count(),
        'usuario': request.user,
        'fecha_exportacion': ahora(),
    }

    html_string = render_to_string(
        'backoffice/tipo_habitacion/tipo_habitacion_pdf.html',
        context
    )

    pdf = HTML(string=html_string).write_pdf()
    return pdf

@login_required
@permission_required("rooms.view_tipohabitacion", raise_exception=True)
@require_safe
def index_tipo_habitacion(request):
    tipos = TipoHabitacion.objects.all()

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_tipo_habitacion(tipos, request)

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"tipos_habitacion_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    ct = ContentType.objects.get_for_model(TipoHabitacion)
    fecha = ahora().date()

    for t in tipos:
        t.tarifa_vigente = get_tarifa_vigente(ct, t.id, fecha)
    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_index.html", {
        "tipos": tipos
    })

@login_required
@permission_required("rooms.add_tipohabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_tipo_habitacion(request):
    form = TipoHabitacionCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        tipo = form.save(commit=False)
        tipo.created_by = request.user
        tipo.updated_by = request.user
        tipo.save()

        return redirect(TIPO_HABITACION_INDEX)

    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_create.html", {
        "form": form
    })

@login_required
@permission_required("rooms.change_tipohabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_tipo_habitacion(request, pk):
    tipo = get_object_or_404(TipoHabitacion, pk=pk, is_active=True)

    form = TipoHabitacionUpdateForm(request.POST or None, instance=tipo)

    if request.method == "POST" and form.is_valid():
        tipo = form.save(commit=False)
        tipo.updated_by = request.user
        tipo.save()

        return redirect(TIPO_HABITACION_INDEX)

    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_update.html", {
        "form": form,
        "tipo": tipo
    })

@login_required
@permission_required("rooms.delete_tipohabitacion", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_tipo_habitacion(request, pk):
    tipo = get_object_or_404(TipoHabitacion, pk=pk, is_active=True)

    form = TipoHabitacionDeleteForm(request.POST or None, tipo=tipo)

    if request.method == "POST" and form.is_valid():
        tipo.is_active = False
        tipo.updated_by = request.user
        tipo.save()

        return redirect(TIPO_HABITACION_INDEX)

    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_delete.html", {
        "form": form,
        "tipo": tipo
    })

@login_required
@permission_required("rooms.view_tipohabitacion", raise_exception=True)
@require_safe
def trashcan_tipo_habitacion(request):
    tipos = TipoHabitacion.all_objects.filter(is_active=False)

    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_trashcan.html", {
        "tipos": tipos
    })

@login_required
@permission_required("rooms.change_tipohabitacion", raise_exception=True)
@require_http_methods(['GET', 'POST'])
def restore_tipo_habitacion(request, pk):
    tipo = get_object_or_404(
        TipoHabitacion.all_objects,
        pk=pk,
        is_active=False
    )

    form = TipoHabitacionRestoreForm(request.POST or None, tipo=tipo)

    if request.method == "POST" and form.is_valid():
        tipo.restore(user=request.user)
        return redirect("rooms:tipo_habitacion_trashcan")

    return render(request, "backoffice/tipo_habitacion/tipo_habitacion_restore.html", {
        "form": form,
        "tipo": tipo
    })