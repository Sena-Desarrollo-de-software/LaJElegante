from django import forms
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from .models import Tarifa
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
        """Asigna los valores antes de guardar"""
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