from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from .models import Tarifa, Impuesto
from core.constants import SERVICIOS_TARIFABLES

class TarifaAdminForm(forms.ModelForm):
    servicio_selector = forms.ChoiceField(
        label="Servicio",
        help_text="Selecciona el servicio que tendrá esta tarifa"
    )
    
    class Meta:
        model = Tarifa
        fields = '__all__'
        widgets = {
            'servicio_id': forms.HiddenInput(),
            'servicio_tipo': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        opciones = []
        
        for (app_label, model_name), info in SERVICIOS_TARIFABLES.items():
            try:
                model = apps.get_model(app_label, info['model'])
                ct = ContentType.objects.get(app_label=app_label, model=model_name)
                servicios = model.objects.filter(is_active=True)
                
                for servicio in servicios:
                    opciones.append((
                        f"{ct.id}|{servicio.id}",
                        f"{info['emoji']} {servicio} ({info['nombre']})"
                    ))
            except Exception:
                pass
        
        self.fields['servicio_selector'].choices = opciones
        
        # Si es edición, seleccionar la opción actual
        if self.instance and self.instance.pk:
            if self.instance.servicio_tipo_id and self.instance.servicio_id:
                valor_actual = f"{self.instance.servicio_tipo_id}|{self.instance.servicio_id}"
                self.fields['servicio_selector'].initial = valor_actual
    
    def clean(self):
        cleaned_data = super().clean()
        servicio_selector = cleaned_data.get('servicio_selector')
        
        if servicio_selector:
            try:
                tipo_id, servicio_id = servicio_selector.split('|')
                content_type = ContentType.objects.get(id=int(tipo_id))
                
                # Asignar a cleaned_data
                cleaned_data['servicio_tipo'] = content_type
                cleaned_data['servicio_id'] = int(servicio_id)
                
            except (ValueError, TypeError, ContentType.DoesNotExist) as e:
                raise forms.ValidationError(f"Error al seleccionar el servicio: {e}")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Obtener los valores del cleaned_data
        if hasattr(self, 'cleaned_data'):
            if 'servicio_tipo' in self.cleaned_data:
                instance.servicio_tipo = self.cleaned_data['servicio_tipo']
                instance.servicio_id = self.cleaned_data['servicio_id']
                print(f"Asignado: servicio_tipo={instance.servicio_tipo}, servicio_id={instance.servicio_id}")
        
        if commit:
            instance.save()
            self.save_m2m()
        
        return instance

class ImpuestoCreateForm(forms.ModelForm):
    class Meta:
        model = Impuesto
        fields = ['nombre', 'tipo', 'porcentaje', 'aplica_a', 'es_obligatorio', 
                  'aplica_extranjeros', 'requiere_informacion_adicional', 
                  'texto_informativo', 'fecha_vigencia_inicio', 'fecha_vigencia_fin']
        widgets = {
            'fecha_vigencia_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_vigencia_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_porcentaje(self):
        porcentaje = self.cleaned_data.get('porcentaje')
        if porcentaje <= 0:
            raise forms.ValidationError("El porcentaje debe ser mayor a 0.")
        return porcentaje

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        nombre = cleaned_data.get('nombre')
        if tipo != 'PROPINA':
            qs = Impuesto.objects.filter(nombre=nombre, tipo=tipo, is_active=True)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Ya existe un impuesto con este nombre y tipo. Use otro nombre.")

        return cleaned_data


class ImpuestoUpdateForm(ImpuestoCreateForm):
    def clean(self):
        cleaned_data = super().clean()
        if self.instance and self.instance.pk:
            if self.instance.tarifaimpuesto_set.filter(is_active=True).exists():
                raise forms.ValidationError(
                    "No se puede modificar este impuesto porque está siendo usado por tarifas activas. "
                    "Archive las tarifas primero o cree un nuevo impuesto."
                )

        return cleaned_data


class ImpuestoDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el nombre del impuesto para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.impuesto = kwargs.pop("impuesto")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip()
        if self.impuesto.nombre != value:
            raise forms.ValidationError("El nombre no coincide.")
        return value

    def clean(self):
        cleaned_data = super().clean()

        if self.impuesto.tarifaimpuesto_set.filter(is_active=True).exists():
            raise forms.ValidationError(
                "No se puede archivar este impuesto porque está siendo usado por tarifas activas. "
                "Archive o espere a que esas tarifas dejen de estar vigentes."
            )

        return cleaned_data


class ImpuestoRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo reincorporar este impuesto"
    )

    def __init__(self, *args, **kwargs):
        self.impuesto = kwargs.pop("impuesto")
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        # Verificar si hay otro impuesto activo con el mismo nombre y tipo
        if Impuesto.objects.filter(
            nombre=self.impuesto.nombre,
            tipo=self.impuesto.tipo,
            is_active=True
        ).exists():
            raise forms.ValidationError(
                "No se puede reincorporar porque ya existe un impuesto activo con el mismo nombre y tipo."
            )

        return cleaned_data