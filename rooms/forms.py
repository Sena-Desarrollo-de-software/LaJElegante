from django import forms
from .models import Habitacion

class HabitacionCreateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado_habitacion"]

    def clean_numero_habitacion(self):
        num = self.cleaned_data["numero_habitacion"]
        # Como el modelo tiene unique=True, NO se puede repetir ni aunque esté inactiva
        if Habitacion.objects.filter(numero_habitacion=num).exists():
            raise forms.ValidationError("Ya existe una habitación con ese número.")
        return num


class HabitacionUpdateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado_habitacion"]

    def clean_numero_habitacion(self):
        num = self.cleaned_data["numero_habitacion"]
        qs = Habitacion.objects.filter(numero_habitacion=num, is_active=True)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Ya existe una habitación activa con ese número.")
        return num


class HabitacionDeleteForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo eliminar (soft delete) esta habitación"
    )
    