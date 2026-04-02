from django import forms
from .models import Horario


class HorarioCreateForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ["turno", "hora_inicio", "hora_fin", "capacidad_maxima"]

    def clean_turno(self):
        turno = self.cleaned_data["turno"]

        if Horario.all_objects.filter(turno=turno).exists():
            raise forms.ValidationError(
                "Ya existe un horario con esa franja (activo o eliminado)."
            )

        return turno

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError(
                "La hora de inicio debe ser menor que la hora de fin."
            )

        return cleaned_data


class HorarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ["turno", "hora_inicio", "hora_fin", "capacidad_maxima"]

    def clean_turno(self):
        turno = self.cleaned_data["turno"]
        qs = Horario.objects.filter(turno=turno)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError(
                "Ya existe un horario activo con esa franja."
            )

        return turno

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fin = cleaned_data.get("hora_fin")

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError(
                "La hora de inicio debe ser menor que la hora de fin."
            )

        return cleaned_data


class HorarioDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe la franja horaria para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.horario = kwargs.pop("horario")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip().upper()

        if self.horario.turno != value:
            raise forms.ValidationError(
                "La franja horaria no coincide."
            )

        return value


class HorarioRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo restaurar este horario"
    )

    def __init__(self, *args, **kwargs):
        self.horario = kwargs.pop("horario")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Horario.objects.filter(turno=self.horario.turno).exists():
            raise forms.ValidationError(
                "Ya existe un horario activo con esta franja."
            )

        return cleaned_data