from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.utils.timezone import localtime

Usuario = get_user_model()

class ProfileUpdateForm(forms.ModelForm):
    date_joined_display = forms.DateTimeField(
        label="Fecha de registro",
        required=False,
        disabled=True,
        initial=None,
    )
    updated_at_display = forms.DateTimeField(
        label="Última actualización",
        required=False,
        disabled=True,
        initial=None,
    )
    is_staff_display = forms.BooleanField(
        label="Usuario staff",
        required=False,
        disabled=True,
        initial=False
    )
    is_superuser_display = forms.BooleanField(
        label="Superusuario",
        required=False,
        disabled=True,
        initial=False
    )
    is_active_display = forms.BooleanField(
        label="Activo",
        required=False,
        disabled=True,
        initial=False
    )
    grupos_display = forms.CharField(
        label="Grupos",
        required=False,
        disabled=True,
        initial=""
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['date_joined_display'].initial = localtime(self.instance.date_joined).strftime('%Y-%m-%d %H:%M')
            self.fields['updated_at_display'].initial = localtime(self.instance.updated_at).strftime('%Y-%m-%d %H:%M')
            self.fields['is_staff_display'].initial = self.instance.is_staff
            self.fields['is_superuser_display'].initial = self.instance.is_superuser
            self.fields['is_active_display'].initial = self.instance.is_active
            self.fields['grupos_display'].initial = ", ".join([g.name for g in self.instance.groups.all()])

    def clean_email(self):
        email = self.cleaned_data.get('email')
        return self.instance.__class__.objects.normalize_email(email)

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="Contraseña actual",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}),
    )
    new_password1 = forms.CharField(
        label="Nueva contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Nueva contraseña'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        label="Repetir nueva contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir nueva contraseña'}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current = self.cleaned_data.get('current_password')
        if not self.user.check_password(current):
            raise forms.ValidationError("La contraseña actual es incorrecta.")
        return current

    def clean(self):
        cleaned = super().clean()
        pw1 = cleaned.get('new_password1')
        pw2 = cleaned.get('new_password2')

        if not pw1 and not pw2:
            return cleaned
        if pw1 and pw2 and pw1 != pw2:
            raise forms.ValidationError("Las contraseñas nuevas no coinciden.")

        password_validation.validate_password(pw1, self.user)
        return cleaned

    def save(self):
        self.user.set_password(self.cleaned_data['new_password1'])
        self.user.save()