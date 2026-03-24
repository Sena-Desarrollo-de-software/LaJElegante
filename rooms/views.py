from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST, require_safe, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Habitacion
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm

HABITACION_LIST_REDIRECT = "rooms:habitacion_list"

# === HABITACIÓN ===
@require_safe
@login_required
def index_habitacion(request):
    habitaciones = Habitacion.objects.filter(is_active=True).order_by("numero_habitacion")
    return render(request, "backoffice/habitaciones/habitacion_index.html", {"habitaciones": habitaciones})

@require_http_methods(["GET", "POST"])
@login_required
@csrf_protect
def create_habitacion(request):
    if request.method == "POST":
        return handle_create_habitacion_post(request)
    else:
        return handle_create_habitacion_get(request)

def handle_create_habitacion_post(request):
    form = HabitacionCreateForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect(HABITACION_LIST_REDIRECT)
    return render(request, "backoffice/habitaciones/habitacion_create.html", {"form": form})

def handle_create_habitacion_get(request):
    form = HabitacionCreateForm()
    return render(request, "backoffice/habitaciones/habitacion_create.html", {"form": form})

@require_http_methods(["GET", "POST"])
@login_required
@csrf_protect
def update_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)
    
    if request.method == "POST":
        return handle_update_habitacion_post(request, habitacion)
    else:
        return handle_update_habitacion_get(request, habitacion)

def handle_update_habitacion_post(request, habitacion):
    form = HabitacionUpdateForm(request.POST, instance=habitacion)
    if form.is_valid():
        form.save()
        return redirect(HABITACION_LIST_REDIRECT)
    return render(request, "backoffice/habitaciones/habitacion_update.html", {"form": form, "habitacion": habitacion})

def handle_update_habitacion_get(request, habitacion):
    form = HabitacionUpdateForm(instance=habitacion)
    return render(request, "backoffice/habitaciones/habitacion_update.html", {"form": form, "habitacion": habitacion})

@require_POST
@login_required
@csrf_protect
def delete_habitacion(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)
    return handle_delete_habitacion_post(request, habitacion)

def handle_delete_habitacion_post(request, habitacion):
    form = HabitacionDeleteForm(request.POST)
    if form.is_valid():
        habitacion.is_active = False
        habitacion.deleted_at = timezone.now()
        habitacion.save(update_fields=["is_active", "deleted_at"])
        return redirect(HABITACION_LIST_REDIRECT)
    return render(request, "backoffice/habitaciones/habitacion_delete.html", {"form": form, "habitacion": habitacion})

@require_http_methods(['POST','GET'])
def trashcan_habitacion(request):
    return render(request,'backoffice/habitaciones/habitacion_trashcan.html')

# === RESERVA RESTAURANTE ===
@require_GET
def index_reserva_restaurante(request):
    return render(request,'backoffice/reserva_restaurante/reserva_restaurante_index.html')

@require_POST
def create_reserva_restaurante(request):
    return render(request,'backoffice/reserva_restaurante/reserva_restaurante_create.html')

@require_http_methods(['POST','GET'])
def update_reserva_restaurante(request):
    return render(request,'backoffice/reserva_restaurante/reserva_restaurante_update.html')

@require_http_methods(['POST','GET'])
def delete_reserva_restaurante(request):
    return render(request, 'backoffice/reserva_restaurante/reserva_restaurante_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_reserva_restaurante(request):
    return render(request,'backoffice/reserva_restaurante/reserva_restaurante_trashcan.html')

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