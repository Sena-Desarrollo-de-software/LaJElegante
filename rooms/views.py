from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .models import Habitacion
from .forms import HabitacionCreateForm, HabitacionUpdateForm, HabitacionDeleteForm


def habitacion_list(request):
    habitaciones = Habitacion.objects.filter(is_active=True).order_by("numero_habitacion")
    return render(request, "rooms/habitacion_list.html", {"habitaciones": habitaciones})


def habitacion_create(request):
    if request.method == "POST":
        form = HabitacionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("rooms:habitacion_list")
    else:
        form = HabitacionCreateForm()
    return render(request, "rooms/habitacion_create.html", {"form": form})

def habitacion_update(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)

    if request.method == "POST":
        form = HabitacionUpdateForm(request.POST, instance=habitacion)
        if form.is_valid():
            form.save()
            return redirect("rooms:habitacion_list")
    else:
        form = HabitacionUpdateForm(instance=habitacion)

    return render(request, "rooms/habitacion_update.html", {"form": form, "habitacion": habitacion})


def habitacion_delete(request, pk):
    habitacion = get_object_or_404(Habitacion, pk=pk, is_active=True)

    if request.method == "POST":
        form = HabitacionDeleteForm(request.POST)
        if form.is_valid():
            habitacion.is_active = False
            habitacion.deleted_at = timezone.now()
            habitacion.save(update_fields=["is_active", "deleted_at"])
            return redirect("rooms:habitacion_list")
    else:
        form = HabitacionDeleteForm()

    return render(request, "rooms/habitacion_delete.html", {"form": form, "habitacion": habitacion})
