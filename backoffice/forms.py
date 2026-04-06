from core.models import Reserva
from django import forms

class ReservaCreateForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['usuario', 'estado']
        widgets = {
            'usuario': forms.Select(attrs={
                'class': 'form-select'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        labels = {
            'usuario': 'Huésped',
            'estado': 'Estado de la reserva',
        }

    def clean_estado(self):
        estado = self.cleaned_data.get('estado')
        if estado != 'PENDIENTE':
            raise forms.ValidationError("Las reservas deben crearse como pendientes.")
        return estado

    def save(self, commit=True, user=None):
        reserva = super().save(commit=False)

        if user:
            reserva.created_by = user
            reserva.updated_by = user

        if commit:
            reserva.save()

        return reserva