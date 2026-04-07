from django import forms
from .models import Horario, Turno, ReservaRestaurante
from core.utils import ahora, combinar_fecha_hora
from users.models import Usuario
from .constants import TIEMPO_LIMITE_RESTAURANTE_HORAS, CAPACIDAD_MAXIMA_TURNO
from datetime import timedelta

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
    
class TurnoCreateForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['horario', 'fecha', 'capacidad_maxima']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['horario'].queryset = Horario.objects.filter(is_active=True)

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < ahora().date():
            raise forms.ValidationError("No se puede crear un turno en una fecha pasada.")
        return fecha

    def clean(self):
        cleaned_data = super().clean()
        horario = cleaned_data.get('horario')
        fecha = cleaned_data.get('fecha')

        if horario and fecha:
            if Turno.objects.filter(horario=horario, fecha=fecha).exists():
                raise forms.ValidationError("Ya existe un turno para ese horario en esa fecha.")

        return cleaned_data


class TurnoUpdateForm(forms.ModelForm):
    class Meta:
        model = Turno
        fields = ['capacidad_maxima']

    def __init__(self, *args, **kwargs):
        self.turno = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.turno and self.turno.reservas.filter(estado__in=['PENDIENTE', 'CONFIRMADA']).exists():
            raise forms.ValidationError(
                "No se puede modificar la capacidad de un turno con reservas activas. "
                "Cancele las reservas o archive el turno y cree otro."
            )

        return cleaned_data


class TurnoDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el ID del turno para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.turno = kwargs.pop("turno")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip()
        if str(self.turno.id) != value:
            raise forms.ValidationError("El ID no coincide.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        if self.turno.reservas.filter(estado__in=['PENDIENTE', 'CONFIRMADA']).exists():
            raise forms.ValidationError(
                "No se puede archivar un turno con reservas activas. "
                "Espere a que se completen o cancelen."
            )

        return cleaned_data


class TurnoRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo reincorporar este turno"
    )

    def __init__(self, *args, **kwargs):
        self.turno = kwargs.pop("turno")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Turno.objects.filter(
            horario=self.turno.horario,
            fecha=self.turno.fecha,
            is_active=True
        ).exists():
            raise forms.ValidationError(
                "No se puede reincorporar porque ya hay otro turno activo para esa misma fecha y horario."
            )

        return cleaned_data
    
class ReservaRestauranteCreateForm(forms.ModelForm):
    class Meta:
        model = ReservaRestaurante
        fields = ['turno', 'cantidad', 'descuento', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar turnos activos y con fecha futura
        self.fields['turno'].queryset = Turno.objects.filter(
            is_active=True,
            fecha__gte=ahora().date()
        ).select_related('horario')

    def clean_turno(self):
        turno = self.cleaned_data.get('turno')
        if turno and turno.fecha < ahora().date():
            raise forms.ValidationError("No se puede reservar en una fecha pasada.")
        return turno

    def clean(self):
        cleaned_data = super().clean()
        turno = cleaned_data.get('turno')
        cantidad = cleaned_data.get('cantidad')

        if turno and cantidad:
            # Validar capacidad disponible
            if not turno.disponible(cantidad):
                raise forms.ValidationError(
                    f"No hay suficiente capacidad disponible en el turno seleccionado. "
                    f"Disponible: {turno.capacidad_disponible}"
                )

        return cleaned_data


class ReservaRestauranteUpdateForm(forms.ModelForm):
    class Meta:
        model = ReservaRestaurante
        fields = ['turno', 'cantidad', 'descuento', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar turnos activos (incluyendo el actual)
        qs = Turno.objects.filter(is_active=True).select_related('horario')
        if self.instance and self.instance.turno:
            qs = qs | Turno.objects.filter(pk=self.instance.turno.pk)
        self.fields['turno'].queryset = qs

    def clean_turno(self):
        turno = self.cleaned_data.get('turno')
        if turno and turno.fecha < ahora().date():
            raise forms.ValidationError("No se puede cambiar a un turno en fecha pasada.")
        return turno

    def clean(self):
        cleaned_data = super().clean()
        nuevo_turno = cleaned_data.get('turno')
        nueva_cantidad = cleaned_data.get('cantidad')

        if not self.instance:
            return cleaned_data

        # Validar límite de modificación
        fecha_reserva = combinar_fecha_hora(
            self.instance.turno.fecha,
            self.instance.turno.horario.hora_inicio
        )
        limite = fecha_reserva - timedelta(hours=TIEMPO_LIMITE_RESTAURANTE_HORAS)
        if ahora() > limite:
            raise forms.ValidationError(
                f"Las reservas solo pueden modificarse hasta "
                f"{TIEMPO_LIMITE_RESTAURANTE_HORAS} horas antes del servicio."
            )

        if fecha_reserva < ahora():
            raise forms.ValidationError("No se puede modificar una reserva que ha expirado.")

        # Si cambia de turno o cantidad, validar disponibilidad del nuevo turno
        if nuevo_turno and nueva_cantidad:
            if nuevo_turno.pk != self.instance.turno.pk:
                if not nuevo_turno.disponible(nueva_cantidad):
                    raise forms.ValidationError(
                        f"No hay suficiente capacidad en el turno seleccionado. "
                        f"Disponible: {nuevo_turno.capacidad_disponible}"
                    )
            elif nueva_cantidad != self.instance.cantidad:
                diferencia = nueva_cantidad - self.instance.cantidad
                if diferencia > 0 and not self.instance.turno.disponible(diferencia):
                    raise forms.ValidationError(
                        f"No hay suficiente capacidad disponible para aumentar la cantidad. "
                        f"Disponible: {self.instance.turno.capacidad_disponible}"
                    )

        return cleaned_data


class ReservaRestauranteCancelForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo cancelar esta reserva"
    )

    def __init__(self, *args, **kwargs):
        self.reserva = kwargs.pop("reserva")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.reserva.estado == 'COMPLETADA':
            raise forms.ValidationError("No se puede cancelar una reserva ya completada.")
        return cleaned_data


class ReservaRestauranteConfirmForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo marcar esta reserva como confirmada"
    )

    def __init__(self, *args, **kwargs):
        self.reserva = kwargs.pop("reserva")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.reserva.estado != 'PENDIENTE':
            raise forms.ValidationError("Solo se pueden confirmar reservas en estado PENDIENTE.")
        return cleaned_data


class ReservaRestauranteCompletarForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que el cliente asistió a la reserva"
    )

    def __init__(self, *args, **kwargs):
        self.reserva = kwargs.pop("reserva")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if self.reserva.estado not in ['PENDIENTE', 'CONFIRMADA']:
            raise forms.ValidationError("Solo se pueden completar reservas en estado PENDIENTE o CONFIRMADA.")
        return cleaned_data