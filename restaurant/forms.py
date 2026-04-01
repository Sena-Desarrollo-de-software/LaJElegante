from django import forms
from .models import Horario


class HorarioCreateForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['turno', 'hora_inicio', 'hora_fin', 'capacidad_maxima']
        widgets = {
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'turno': 'Franja horaria',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
            'capacidad_maxima': 'Capacidad máxima',
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError('La hora de inicio debe ser menor que la hora de fin.')

        return cleaned_data


class HorarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = ['turno', 'hora_inicio', 'hora_fin', 'capacidad_maxima']
        widgets = {
            'turno': forms.Select(attrs={'class': 'form-control'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'hora_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'capacidad_maxima': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        labels = {
            'turno': 'Franja horaria',
            'hora_inicio': 'Hora de inicio',
            'hora_fin': 'Hora de fin',
            'capacidad_maxima': 'Capacidad máxima',
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fin = cleaned_data.get('hora_fin')

        if hora_inicio and hora_fin and hora_inicio >= hora_fin:
            raise forms.ValidationError('La hora de inicio debe ser menor que la hora de fin.')

        return cleaned_data


class HorarioDeleteForm(forms.ModelForm):
    class Meta:
        model = Horario
        fields = []