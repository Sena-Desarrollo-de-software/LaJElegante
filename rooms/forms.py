from django import forms
from .models import Habitacion

class HabitacionCreateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado_habitacion"]

class HabitacionUpdateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado_habitacion"]

class HabitacionDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo eliminar (soft delete) esta habitación"
    )
