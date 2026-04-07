from django import forms
from django.utils import timezone
from rooms.models import ReservaHabitacion, Habitacion
from restaurant.models import ReservaRestaurante, Turno


class GuestReservaHabitacionUpdateForm(forms.ModelForm):
    class Meta:
        model = ReservaHabitacion
        fields = ['habitacion', 'fecha_inicio', 'fecha_fin', 'cantidad_personas', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['habitacion'].queryset = Habitacion.objects.filter(is_active=True)
        self.fields['habitacion'].widget.attrs.update({'class': 'form-select'})


class GuestReservaHabitacionCreateForm(forms.ModelForm):
    class Meta:
        model = ReservaHabitacion
        fields = ['habitacion', 'fecha_inicio', 'fecha_fin', 'cantidad_personas', 'observaciones']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'cantidad_personas': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        fecha_inicio = kwargs.pop('fecha_inicio', None)
        fecha_fin = kwargs.pop('fecha_fin', None)

        super().__init__(*args, **kwargs)

        habitaciones = Habitacion.objects.filter(
            is_active=True,
            estado='DISPONIBLE'
        ).select_related('tipo_habitacion')

        if fecha_inicio and fecha_fin:
            disponibles_ids = [
                h.id for h in habitaciones
                if h.disponible_en_fechas(fecha_inicio, fecha_fin)
            ]

            habitaciones = Habitacion.objects.filter(id__in=disponibles_ids)

            if not disponibles_ids:
                self.fields['habitacion'].help_text = 'No hay habitaciones disponibles en esas fechas'

        self.fields['habitacion'].queryset = habitaciones
        self.fields['habitacion'].widget.attrs.update({'class': 'form-select'})


class GuestReservaRestauranteForm(forms.ModelForm):
    class Meta:
        model = ReservaRestaurante
        fields = ['turno', 'cantidad', 'observaciones']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoy = timezone.localdate()
        self.fields['turno'].queryset = Turno.objects.filter(is_active=True, fecha__gte=hoy).select_related('horario')
        self.fields['turno'].widget.attrs.update({'class': 'form-select'})
