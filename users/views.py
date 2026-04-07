from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm, ChangePasswordForm
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.conf import settings

app_name = 'rooms'

# === USUARIO ===
@require_GET
def index_usuario(request):
    return render(request,'backoffice/usuarios/usuario_index.html')

@require_POST
def create_usuario(request):
    return render(request,'backoffice/usuarios/usuario_create.html')

@require_http_methods(['POST','GET'])
def update_usuario(request):
    return render(request,'backoffice/usuarios/usuario_update.html')

@require_http_methods(['POST','GET'])
def delete_usuario(request):
    return render(request, 'backoffice/usuarios/usuario_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_usuario(request):
    return render(request,'backoffice/usuarios/usuario_trashcan.html')

# === GRUPO ===
@require_GET
def index_grupo(request):
    return render(request,'backoffice/grupos/grupo_index.html')

@require_POST
def create_grupo(request):
    return render(request,'backoffice/grupos/grupo_create.html')

@require_http_methods(['POST','GET'])
def update_grupo(request):
    return render(request,'backoffice/grupos/grupo_update.html')

@require_http_methods(['POST','GET'])
def delete_grupo(request):
    return render(request, 'backoffice/grupos/grupo_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_grupo(request):
    return render(request,'backoffice/grupos/grupo_trashcan.html')

#Metodo de actualizacion de perfil
def redirect_after_profile_update(user):
    if user.groups.filter(name='Clientes').exists():
        return redirect('guest:profile_update', pk=user.id)
    else:
        return redirect('users:profile_update', pk=user.id)

@login_required
def update_usuario_auto(request, pk):
    if request.user.pk != pk:
        messages.error(request, "No puedes editar el perfil de otro usuario.")
        return redirect_after_profile_update(request.user)

    user = request.user
    if request.method == 'POST':
        profile_form = ProfileUpdateForm(request.POST, instance=user)
        password_form = ChangePasswordForm(user, request.POST)

        if 'update_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect_after_profile_update(user)

        elif 'change_password' in request.POST and password_form.is_valid():
            password_form.save()
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect_after_profile_update(user)

    else:
        profile_form = ProfileUpdateForm(instance=user)
        password_form = ChangePasswordForm(user)

    context = {
        'form': profile_form,
        'password_form': password_form,
    }
    return render(request, 'backoffice/profile/profile_update.html', context)

@login_required
def send_password_reset_email(request):
    user_email = request.user.email

    if not user_email:
        messages.error(request, "No tienes un correo asociado a tu cuenta.")
        return render(request, 'backoffice/profile/profile_update.html', {'form': ProfileUpdateForm(instance=request.user)})

    form = PasswordResetForm({'email': user_email})
    if form.is_valid():
        form.save(
            request=request,
            use_https=request.is_secure(),
            from_email=settings.FROM_EMAILS['ayuda'],
            email_template_name='hotel/password_reset_email.txt',
            html_email_template_name='hotel/password_reset_email.html',
        )
        messages.success(request, "Se ha enviado un enlace de cambio de contraseña a tu correo.")
    else:
        messages.error(request, "No se pudo generar el enlace de cambio de contraseña.")

    return render(request, 'backoffice/profile/profile_update.html', {'form': ProfileUpdateForm(instance=request.user)})