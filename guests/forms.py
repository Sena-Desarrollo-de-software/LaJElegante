from django import forms
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.db.models import F, Q
from rooms.models import ReservaHabitacion, Habitacion
from restaurant.models import ReservaRestaurante, Turno, Horario
from finance.models import Tarifa


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
    fecha = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        label='Fecha'
    )

    class Meta:
        model = ReservaRestaurante
        fields = ['turno', 'cantidad', 'observaciones']
        labels = {
            'turno': 'Turno disponible',
            'cantidad': 'Cantidad de personas',
            'observaciones': 'Observaciones',
        }
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        hoy = timezone.localdate()

        fecha_str = None
        if self.is_bound:
            fecha_str = self.data.get('fecha')

        fecha = self.initial.get('fecha')
        if self.instance and self.instance.pk and self.instance.turno_id:
            fecha = self.instance.turno.fecha
        if fecha_str:
            try:
                fecha = forms.DateField().to_python(fecha_str)
            except forms.ValidationError:
                fecha = None

        self.fields['fecha'].initial = fecha
        self.fields['fecha'].widget.attrs.update({'min': hoy.isoformat()})

        turnos_qs = Turno.objects.none()
        if fecha:
            ct_horario = ContentType.objects.get_for_model(Horario)
            horarios_con_tarifa = Tarifa.objects.filter(
                servicio_tipo=ct_horario,
                estado='VIGENTE',
                temporada__fecha_inicio__lte=fecha,
                temporada__fecha_fin__gte=fecha,
            ).values_list('servicio_id', flat=True)

            turnos_qs = Turno.objects.filter(
                is_active=True,
                fecha=fecha,
                horario_id__in=horarios_con_tarifa,
            ).select_related('horario')

            # Solo mostrar turnos con al menos 1 cupo disponible.
            turnos_qs = turnos_qs.filter(
                Q(capacidad_maxima__isnull=True, quorum__lt=F('horario__capacidad_maxima')) |
                Q(capacidad_maxima__isnull=False, quorum__lt=F('capacidad_maxima'))
            )

        if self.instance and self.instance.pk and self.instance.turno_id:
            turnos_qs = (turnos_qs | Turno.objects.filter(pk=self.instance.turno_id).select_related('horario')).distinct()

        self.fields['turno'].queryset = turnos_qs
        self.fields['turno'].widget.attrs.update({'class': 'form-select'})
        self.fields['turno'].empty_label = 'Selecciona un turno'
        self.fields['cantidad'].help_text = 'Este valor descuenta cupos del turno seleccionado.'
        self.fields['turno'].label_from_instance = (
            lambda obj: f"{obj.horario.get_turno_display()} | {obj.fecha} | {obj.horario.hora_inicio.strftime('%H:%M')} - {obj.horario.hora_fin.strftime('%H:%M')} | Cupos: {obj.capacidad_disponible}/{obj.capacidad_efectiva}"
        )

        if not fecha:
            self.fields['turno'].help_text = 'Primero selecciona una fecha para ver turnos disponibles.'
        elif not self.fields['turno'].queryset.exists():
            self.fields['turno'].help_text = 'No hay turnos disponibles con tarifa vigente para la fecha seleccionada.'

    def clean(self):
        cleaned_data = super().clean()
        fecha = cleaned_data.get('fecha')
        turno = cleaned_data.get('turno')
        cantidad = cleaned_data.get('cantidad')

        if turno and fecha and turno.fecha != fecha:
            self.add_error('turno', 'El turno seleccionado no corresponde a la fecha indicada.')

        if turno and turno.capacidad_disponible <= 0:
            self.add_error('turno', 'Este turno ya no tiene cupos disponibles.')

        if turno and cantidad and not turno.disponible(cantidad):
            self.add_error('cantidad', f'No hay cupo disponible. Solo quedan {turno.capacidad_disponible} lugares.')

        return cleaned_data
