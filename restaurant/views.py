from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_GET, require_POST, require_http_methods, require_safe
from django.views.decorators.csrf import csrf_protect

from .models import Horario
from .forms import (
    HorarioCreateForm,
    HorarioUpdateForm,
    HorarioDeleteForm,
    HorarioRestoreForm,
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


# === MESA ===
@require_GET
def index_turno(request):
    return render(request, 'backoffice/turnos/turno_index.html')


@require_POST
def create_turno(request):
    return render(request, 'backoffice/turnos/turno_create.html')


@require_http_methods(['POST', 'GET'])
def update_turno(request):
    return render(request, 'backoffice/turnos/turno_update.html')


@require_http_methods(['POST', 'GET'])
def delete_turno(request):
    return render(request, 'backoffice/turnos/turno_delete.html')


@require_http_methods(['POST', 'GET'])
def trashcan_turno(request):
    return render(request, 'backoffice/turnos/turno_trashcan.html')


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