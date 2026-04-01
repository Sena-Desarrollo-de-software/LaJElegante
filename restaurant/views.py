from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.utils import timezone

from .forms import HorarioCreateForm, HorarioUpdateForm, HorarioDeleteForm
from .models import Horario


# === HORARIO ===
@require_GET
def index_horario(request):
    horarios = Horario.objects.filter(is_active=True).order_by('hora_inicio')
    return render(request, 'backoffice/horarios/horario_index.html', {
        'horarios': horarios
    })


@require_http_methods(['GET', 'POST'])
def create_horario(request):
    if request.method == 'POST':
        form = HorarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('restaurant:horario_index')
    else:
        form = HorarioCreateForm()

    return render(request, 'backoffice/horarios/horario_create.html', {
        'form': form,
        'titulo': 'Crear horario'
    })


@require_http_methods(['GET', 'POST'])
def update_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk, is_active=True)

    if request.method == 'POST':
        form = HorarioUpdateForm(request.POST, instance=horario)
        if form.is_valid():
            form.save()
            return redirect('restaurant:horario_index')
    else:
        form = HorarioUpdateForm(instance=horario)

    return render(request, 'backoffice/horarios/horario_update.html', {
        'form': form,
        'horario': horario,
        'titulo': 'Actualizar horario'
    })


@require_http_methods(['GET', 'POST'])
def delete_horario(request, pk):
    horario = get_object_or_404(Horario, pk=pk, is_active=True)

    if request.method == 'POST':
        form = HorarioDeleteForm(request.POST, instance=horario)
        if form.is_valid():
            horario.is_active = False
            horario.deleted_at = timezone.now()
            horario.save()
            return redirect('restaurant:horario_index')
    else:
        form = HorarioDeleteForm(instance=horario)

    return render(request, 'backoffice/horarios/horario_delete.html', {
        'form': form,
        'horario': horario
    })


@require_GET
def trashcan_horario(request):
    horarios = Horario.objects.filter(is_active=False).order_by('-deleted_at')
    return render(request, 'backoffice/horarios/horario_trashcan.html', {
        'horarios': horarios
    })


# === MESA ===
@require_GET
def index_turno(request):
    return render(request, 'backoffice/turnos/turno_index.html')


@require_POST
def create_turno(request):
    return render(request, 'backoffice/turnos/turno_create.html')


@require_http_methods(['POST', 'GET'])
def update_turno(request, pk=None):
    return render(request, 'backoffice/turnos/turno_update.html')


@require_http_methods(['POST', 'GET'])
def delete_turno(request, pk=None):
    return render(request, 'backoffice/turnos/turno_delete.html')


@require_http_methods(['POST', 'GET'])
def trashcan_turno(request, pk=None):
    return render(request, 'backoffice/turnos/turno_trashcan.html')


# === RESERVA RESTAURANTE ===
@require_GET
def index_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_index.html')


@require_POST
def create_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_create.html')


@require_http_methods(['POST', 'GET'])
def update_reserva_restaurante(request, pk=None):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_update.html')


@require_http_methods(['POST', 'GET'])
def delete_reserva_restaurante(request, pk=None):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_delete.html')


@require_http_methods(['POST', 'GET'])
def trashcan_reserva_restaurante(request, pk=None):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_trashcan.html')