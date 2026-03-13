from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST, require_safe
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import Habitacion
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm

HABITACION_LIST_REDIRECT = "rooms:habitacion_list"

@require_safe
@login_required
def habitacion_list(request):
    habitaciones = Habitacion.objects.filter(is_active=True).order_by("numero_habitacion")
    return render(request, "rooms/habitacion_list.html", {"habitaciones": habitaciones})

@require_http_methods(["GET", "POST"])
@login_required
@csrf_protect
def habitacion_create(request):
    if request.method == "POST":
        form = HabitacionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(HABITACION_LIST_REDIRECT)
    else:
        form = HabitacionCreateForm()
    return render(request, "rooms/habitacion_create.html", {"form": form})

@require_http_methods(["GET", "POST"])
@login_required
@csrf_protect
def habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)

    if request.method == "POST":
        form = HabitacionUpdateForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect(HABITACION_LIST_REDIRECT)
    else:
        form = HabitacionUpdateForm(instance=habitacion)

    return render(request, "rooms/habitacion_update.html", {"form": form, "habitacion": habitacion})

@require_POST
@login_required
@csrf_protect
def habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)

    if request.method == "POST":
        form = HabitacionDeleteForm(request.POST)
        if form.is_valid():
            habitacion.is_active = False
            habitacion.deleted_at = timezone.now()
            habitacion.save(update_fields=["is_active", "deleted_at"])
            return redirect(HABITACION_LIST_REDIRECT)
    else:
        form = HabitacionDeleteForm()

    return render(request, "rooms/habitacion_delete.html", {"form": form, "habitacion": habitacion})
