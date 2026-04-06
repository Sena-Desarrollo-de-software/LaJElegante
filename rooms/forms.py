from django import forms
from django.core.exceptions import ValidationError
from .models import Habitacion, TipoHabitacion, ReservaHabitacion

class HabitacionCreateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado"]

    def clean_numero_habitacion(self):
        num = self.cleaned_data["numero_habitacion"]

        if Habitacion.all_objects.filter(numero_habitacion=num).exists():
            raise forms.ValidationError("Ya existe una habitación con ese número (activa o eliminada).")

        return num


class HabitacionUpdateForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ["tipo_habitacion", "numero_habitacion", "estado"]

    def clean_numero_habitacion(self):
        num = self.cleaned_data["numero_habitacion"]
        qs = Habitacion.objects.filter(numero_habitacion=num)

        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe una habitación activa con ese número.")

        return num


class HabitacionDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el número de la habitación para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.habitacion = kwargs.pop("habitacion")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"]

        if str(self.habitacion.numero_habitacion) != value:
            raise forms.ValidationError("El número no coincide.")

        return value

class HabitacionRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo restaurar esta habitación"
    )

    def __init__(self, *args, **kwargs):
        self.habitacion = kwargs.pop("habitacion")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if Habitacion.objects.filter(
            numero_habitacion=self.habitacion.numero_habitacion
        ).exists():
            raise forms.ValidationError("Ya existe una habitación activa con este número.")

        return cleaned_data
    
class HabitacionImportForm(forms.ModelForm):
    class Meta:
        model = Habitacion
        fields = ['numero_habitacion', 'tipo_habitacion', 'estado']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['estado'].required = False
        self.fields['tipo_habitacion'] = forms.CharField(
            label='Tipo de habitación',
            required=True,
            help_text='Escribe el nombre del tipo (FAMILIAR, PAREJA, BASICA, ESPECIAL)'
        )

    def clean_tipo_habitacion(self):
        nombre = self.cleaned_data['tipo_habitacion'].strip().upper()
        mapeo = {
            'FAMILIAR': 'FAMILIAR',
            'PAREJA': 'PAREJA',
            'BASICA': 'BASICA',
            'BÁSICA': 'BASICA',
            'ESPECIAL': 'ESPECIAL',
            'SIMPLE': 'BASICA',
            'DOBLE': 'PAREJA',
            'MATRIMONIAL': 'PAREJA',
            'SUITE': 'ESPECIAL',
        }
        clave = mapeo.get(nombre, nombre)
        try:
            return TipoHabitacion.objects.get(nombre_tipo=clave)
        except TipoHabitacion.DoesNotExist:
            raise forms.ValidationError(f"Tipo '{nombre}' no válido. Usa FAMILIAR, PAREJA, BASICA o ESPECIAL.")

    def clean_estado(self):
        estado = self.cleaned_data.get('estado', 'DISPONIBLE')
        if estado not in dict(Habitacion.ESTADO_HABITACION_CHOICES):
            return 'DISPONIBLE'
        return estado
    
class TipoHabitacionCreateForm(forms.ModelForm):
    class Meta:
        model = TipoHabitacion
        fields = ["nombre_tipo", "descripcion", "capacidad_maxima"]
        widgets = {
            "nombre_tipo": forms.Select(attrs={
                "class": "form-select"
            }),
            "descripcion": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Descripción opcional..."
            }),
            "capacidad_maxima": forms.NumberInput(attrs={
                "class": "form-control",
                "min": 1
            }),
        }

    def clean_nombre_tipo(self):
        nombre = self.cleaned_data["nombre_tipo"]

        if TipoHabitacion.objects.filter(nombre_tipo=nombre).exists():
            raise forms.ValidationError("Ya existe este tipo de habitación.")

        return nombre
    
    def clean_capacidad_maxima(self):
        capacidad = self.cleaned_data["capacidad_maxima"]

        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser mayor a 0.")

        return capacidad

class TipoHabitacionUpdateForm(TipoHabitacionCreateForm):

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance")
        super().__init__(*args, **kwargs)

    def clean_nombre_tipo(self):
        nombre = self.cleaned_data["nombre_tipo"]

        qs = TipoHabitacion.objects.filter(nombre_tipo=nombre)

        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Ya existe este tipo de habitación.")

        return nombre
    
class TipoHabitacionDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el nombre del tipo para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.tipo = kwargs.pop("tipo")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip().upper()

        if self.tipo.nombre_tipo != value:
            raise forms.ValidationError("El nombre no coincide.")

        return value

    def clean(self):
        cleaned_data = super().clean()

        if self.tipo.habitaciones.filter(is_active=True).exists():
            raise forms.ValidationError(
                "No puedes eliminar este tipo porque tiene habitaciones activas."
            )

        return cleaned_data

class TipoHabitacionRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo restaurar este tipo de habitación"
    )

    def __init__(self, *args, **kwargs):
        self.tipo = kwargs.pop("tipo")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.tipo.habitaciones.filter(is_active=True).exists():
            raise forms.ValidationError(
                "No se puede restaurar porque ya existen habitaciones activas con este tipo."
            )

        return cleaned_data

class ReservaHabitacionCreateForm(forms.ModelForm):

    class Meta:
        model = ReservaHabitacion
        fields = [
            'habitacion',
            'fecha_inicio',
            'fecha_fin',
            'cantidad_personas',
            'descuento',
            'observaciones'
        ]

        widgets = {
            "fecha_inicio": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "fecha_fin": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
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
                self.fields['habitacion'].help_text = "No hay habitaciones disponibles en esas fechas"

        self.fields['habitacion'].queryset = habitaciones

    def clean(self):
        cleaned_data = super().clean()

        instance = ReservaHabitacion(
            habitacion=cleaned_data.get("habitacion"),
            fecha_inicio=cleaned_data.get("fecha_inicio"),
            fecha_fin=cleaned_data.get("fecha_fin"),
            cantidad_personas=cleaned_data.get("cantidad_personas"),
            descuento=cleaned_data.get("descuento"),
            observaciones=cleaned_data.get("observaciones"),
        )

        if self.instance.pk:
            instance.pk = self.instance.pk

        try:
            instance.clean()
        except ValidationError as e:
            self.add_error(None, e)

        return cleaned_data
    

class ReservaHabitacionUpdateForm(forms.ModelForm):


    class Meta:
        model = ReservaHabitacion
        fields = [
            'descuento',
            'observaciones'
        ]
        widgets = {
            "observaciones": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            if hasattr(self.instance, 'estado') and self.instance.estado != "PENDIENTE":
                raise ValidationError("Solo se pueden editar reservas en estado PENDIENTE.")
        return cleaned_data