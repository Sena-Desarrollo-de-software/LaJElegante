from django.shortcuts import render
from django import forms

class DummyForm(forms.Form):
    pass

def habitacion_list(request):
    return render(request, "rooms/habitacion_list.html")

def habitacion_create(request):
    form = DummyForm()
    return render(request, "rooms/habitacion_create.html", {"form": form})

def habitacion_update(request, pk):
    form = DummyForm()
    return render(request, "rooms/habitacion_update.html", {"form": form})

def habitacion_delete(request, pk):
    return render(request, "rooms/habitacion_delete.html")
