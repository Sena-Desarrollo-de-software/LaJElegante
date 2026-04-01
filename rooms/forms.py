from django import forms
from .models import Habitacion, TipoHabitacion

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