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

from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from .models import Usuario, GrupoProxy
from django.contrib.auth.models import Group, Permission


class UsuarioCreateForm(UserCreationForm):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label="Grupos/Roles"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_active'].initial = True
        self.fields['is_staff'].initial = False

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if Usuario.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario ya está asociado a otro usuario.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Asignar grupos
            grupos = self.cleaned_data.get('grupos')
            if grupos:
                user.groups.set(grupos)
        return user


class UsuarioUpdateForm(forms.ModelForm):
    grupos = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label="Grupos/Roles"
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['grupos'].initial = self.instance.groups.all()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = Usuario.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("El nombre de usuario ya está asociado a otro usuario.")
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            grupos = self.cleaned_data.get('grupos')
            user.groups.set(grupos)
        return user


class UsuarioDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el nombre de usuario para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip()
        if self.usuario.username != value:
            raise ValidationError("El nombre de usuario no coincide.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        # Verificar si tiene reservas activas
        from core.models import Reserva
        if Reserva.objects.filter(usuario=self.usuario, estado__in=['PENDIENTE', 'CONFIRMADA']).exists():
            raise ValidationError(
                "No se puede archivar el usuario porque tiene reservas activas. "
                "Complete o cancele las reservas primero."
            )
        return cleaned_data


class UsuarioRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo reincorporar este usuario"
    )

    def __init__(self, *args, **kwargs):
        self.usuario = kwargs.pop("usuario")
        super().__init__(*args, **kwargs)


class PerfilUpdateForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'first_name', 'last_name']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Usuario.objects.filter(email=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("El correo electrónico ya está registrado.")
        return email


# === GRUPOS ===
class GrupoCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Group.objects.filter(name=name).exists():
            raise ValidationError("El nombre del grupo ya existe. Use otro nombre.")
        return name


class GrupoUpdateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get('name')
        qs = Group.objects.filter(name=name)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("El nombre del grupo ya existe. Use otro nombre.")
        return name


class GrupoDeleteForm(forms.Form):
    confirm = forms.CharField(
        required=True,
        label="Escribe el nombre del grupo para confirmar"
    )

    def __init__(self, *args, **kwargs):
        self.grupo = kwargs.pop("grupo")
        super().__init__(*args, **kwargs)

    def clean_confirm(self):
        value = self.cleaned_data["confirm"].strip()
        if self.grupo.name != value:
            raise ValidationError("El nombre no coincide.")
        return value

    def clean(self):
        cleaned_data = super().clean()
        if self.grupo.user_set.filter(is_active=True).exists():
            raise ValidationError(
                "No se puede archivar el grupo porque tiene usuarios asignados. "
                "Reasigne o archive los usuarios primero."
            )
        return cleaned_data


class GrupoRestoreForm(forms.Form):
    confirm = forms.BooleanField(
        required=True,
        label="Confirmo que deseo reincorporar este grupo"
    )

    def __init__(self, *args, **kwargs):
        self.grupo = kwargs.pop("grupo")
        super().__init__(*args, **kwargs)