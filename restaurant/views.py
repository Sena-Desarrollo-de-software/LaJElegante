from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from core.utils import ahora
from .models import Horario, Turno
from .forms import (
    HorarioCreateForm,
    HorarioUpdateForm,
    HorarioDeleteForm,
    HorarioRestoreForm,
    TurnoCreateForm,
    TurnoUpdateForm,
    TurnoDeleteForm,
    TurnoRestoreForm,
)

HORARIO_INDEX = "restaurant:horario_index"


# === HORARIO ===
@login_required
@permission_required("restaurant.view_horario", raise_exception=True)
@require_safe
def index_horario(request):
    horarios = Horario.objects.all()

    return render(request, "backoffice/horarios/horario_index.html", {
        "horarios": horarios
    })


@login_required
@permission_required("restaurant.add_horario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_horario(request):
    form = HorarioCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        horario = form.save(commit=False)
        horario.created_by = request.user
        horario.updated_by = request.user
        horario.save()

        return redirect(HORARIO_INDEX)

    return render(request, "backoffice/horarios/horario_create.html", {
        "form": form
    })


@login_required
@permission_required("restaurant.change_horario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_horario(request, pk):
    horario = get_object_or_404(Horario.objects, pk=pk)
    form = HorarioUpdateForm(request.POST or None, instance=horario)

    if form.is_valid():
        horario = form.save(commit=False)
        horario.updated_by = request.user
        horario.save()

        return redirect(HORARIO_INDEX)

    return render(request, "backoffice/horarios/horario_update.html", {
        "form": form,
        "horario": horario
    })


@login_required
@permission_required("restaurant.delete_horario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_horario(request, pk):
    horario = get_object_or_404(Horario.objects, pk=pk)
    form = HorarioDeleteForm(request.POST or None, horario=horario)

    if form.is_valid():
        horario.soft_delete(user=request.user)
        return redirect(HORARIO_INDEX)

    return render(request, "backoffice/horarios/horario_delete.html", {
        "form": form,
        "horario": horario
    })


@login_required
@permission_required("restaurant.delete_horario", raise_exception=True)
@require_safe
def trashcan_horario(request):
    horarios = Horario.all_objects.filter(is_active=False)

    return render(request, "backoffice/horarios/horario_trashcan.html", {
        "horarios": horarios
    })


@login_required
@permission_required("restaurant.change_horario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_horario(request, pk):
    horario = get_object_or_404(
        Horario.all_objects,
        pk=pk,
        is_active=False
    )

    form = HorarioRestoreForm(request.POST or None, horario=horario)

    if form.is_valid():
        horario.restore(user=request.user)
        return redirect("restaurant:horario_trashcan")

    return render(request, "backoffice/horarios/horario_restore.html", {
        "form": form,
        "horario": horario
    })


# === TURNO ===
TURNO_INDEX = "restaurant:turno_index"

def filtrar_turnos(request, queryset=None):
    if queryset is None:
        queryset = Turno.objects.all().select_related('horario')

    horario_id = request.GET.get("horario")
    fecha = request.GET.get("fecha")
    estado = request.GET.get("estado")

    if horario_id:
        queryset = queryset.filter(horario_id=horario_id)

    if fecha:
        queryset = queryset.filter(fecha=fecha)

    if estado == "activo":
        queryset = queryset.filter(is_active=True)
    elif estado == "archivado":
        queryset = queryset.filter(is_active=False)

    return queryset


def generar_pdf_turnos(turnos, filtros, request):
    context = {
        'turnos': turnos,
        'filtros': filtros,
        'total_registros': turnos.count(),
        'usuario': request.user,
        'fecha_exportacion': ahora(),
        'horarios': Horario.objects.all(),
    }
    html_string = render_to_string('backoffice/turnos/turno_pdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf


@login_required
@permission_required("restaurant.view_turno", raise_exception=True)
@require_safe
def index_turno(request):
    turnos = filtrar_turnos(request)

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_turnos(turnos, request.GET, request)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"turnos_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render(request, "backoffice/turnos/turno_index.html", {
        "turnos": turnos,
        "horarios": Horario.objects.filter(is_active=True),
        "filtros": request.GET
    })


@login_required
@permission_required("restaurant.add_turno", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_turno(request):
    form = TurnoCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        turno = form.save(commit=False)
        turno.created_by = request.user
        turno.updated_by = request.user
        turno.save()
        return redirect(TURNO_INDEX)

    return render(request, "backoffice/turnos/turno_create.html", {"form": form})


@login_required
@permission_required("restaurant.change_turno", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_turno(request, pk):
    turno = get_object_or_404(Turno.objects, pk=pk, is_active=True)
    form = TurnoUpdateForm(request.POST or None, instance=turno)

    if request.method == "POST" and form.is_valid():
        turno = form.save(commit=False)
        turno.updated_by = request.user
        turno.save()
        return redirect(TURNO_INDEX)

    return render(request, "backoffice/turnos/turno_update.html", {
        "form": form,
        "turno": turno
    })


@login_required
@permission_required("restaurant.delete_turno", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_turno(request, pk):
    turno = get_object_or_404(Turno.objects, pk=pk, is_active=True)
    form = TurnoDeleteForm(request.POST or None, turno=turno)

    if request.method == "POST" and form.is_valid():
        turno.is_active = False
        turno.updated_by = request.user
        turno.save()
        return redirect(TURNO_INDEX)

    return render(request, "backoffice/turnos/turno_delete.html", {
        "form": form,
        "turno": turno
    })


@login_required
@permission_required("restaurant.view_turno", raise_exception=True)
@require_safe
def trashcan_turno(request):
    turnos = Turno.all_objects.filter(is_active=False).select_related('horario')
    return render(request, "backoffice/turnos/turno_trashcan.html", {"turnos": turnos})


@login_required
@permission_required("restaurant.change_turno", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_turno(request, pk):
    turno = get_object_or_404(Turno.all_objects, pk=pk, is_active=False)
    form = TurnoRestoreForm(request.POST or None, turno=turno)

    if request.method == "POST" and form.is_valid():
        turno.is_active = True
        turno.updated_by = request.user
        turno.save()
        return redirect("restaurant:turno_trashcan")

    return render(request, "backoffice/turnos/turno_restore.html", {
        "form": form,
        "turno": turno
    })

@login_required
@permission_required("restaurant.add_turno", raise_exception=True)
def import_turno(request):
    context = {
        'title': 'Importar Turnos',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
    }

    return render(
        request,
        'backoffice/turnos/turno_import.html',
        context
    )
# === RESERVA RESTAURANTE ===
@require_GET
def index_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_index.html')


@require_POST
def create_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_create.html')


@require_http_methods(['POST', 'GET'])
def update_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_update.html')


@require_http_methods(['POST', 'GET'])
def delete_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_delete.html')


@require_http_methods(['POST', 'GET'])
def trashcan_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_trashcan.html')