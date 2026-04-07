from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods, require_safe, require_POST
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib import messages
from weasyprint import HTML
from django.contrib.auth.models import Group
from core.utils import ahora
from .models import Usuario, GrupoProxy
from .forms import (
    UsuarioCreateForm, UsuarioUpdateForm, UsuarioDeleteForm, UsuarioRestoreForm,
    PerfilUpdateForm, GrupoCreateForm, GrupoUpdateForm, GrupoDeleteForm, GrupoRestoreForm,
    ProfileUpdateForm, ChangePasswordForm
)

USUARIO_INDEX = "users:usuario_index"
GRUPO_INDEX = "users:grupo_index"


# === USUARIOS ===
def filtrar_usuarios(request, queryset=None):
    if queryset is None:
        queryset = Usuario.objects.all()

    username = request.GET.get("username")
    email = request.GET.get("email")
    grupo = request.GET.get("grupo")
    estado = request.GET.get("estado")

    if username:
        queryset = queryset.filter(username__icontains=username)

    if email:
        queryset = queryset.filter(email__icontains=email)

    if grupo:
        queryset = queryset.filter(groups__name=grupo)

    if estado == "activo":
        queryset = queryset.filter(is_active=True)
    elif estado == "archivado":
        queryset = queryset.filter(is_active=False)

    return queryset


def generar_pdf_usuarios(usuarios, filtros, request):
    context = {
        'usuarios': usuarios,
        'filtros': filtros,
        'total_registros': usuarios.count(),
        'usuario': request.user,
        'fecha_exportacion': ahora(),
    }
    html_string = render_to_string('backoffice/usuarios/usuario_pdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf


@login_required
@permission_required("users.view_usuario", raise_exception=True)
@require_safe
def index_usuario(request):
    usuarios = filtrar_usuarios(request)

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_usuarios(usuarios, request.GET, request)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"usuarios_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render(request, "backoffice/usuarios/usuario_index.html", {
        "usuarios": usuarios,
        "grupos": Group.objects.all(),
        "filtros": request.GET
    })


@login_required
@permission_required("users.add_usuario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_usuario(request):
    form = UsuarioCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        messages.success(request, f"Usuario {usuario.username} creado exitosamente.")
        return redirect(USUARIO_INDEX)

    return render(request, "backoffice/usuarios/usuario_create.html", {"form": form})


@login_required
@permission_required("users.change_usuario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_usuario(request, pk):
    usuario = get_object_or_404(Usuario.objects, pk=pk, is_active=True)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)

    if request.method == "POST" and form.is_valid():
        usuario = form.save()
        messages.success(request, f"Usuario {usuario.username} actualizado exitosamente.")
        return redirect(USUARIO_INDEX)

    return render(request, "backoffice/usuarios/usuario_update.html", {
        "form": form,
        "usuario": usuario
    })


@login_required
@permission_required("users.delete_usuario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_usuario(request, pk):
    usuario = get_object_or_404(Usuario.objects, pk=pk, is_active=True)
    form = UsuarioDeleteForm(request.POST or None, usuario=usuario)

    if request.method == "POST" and form.is_valid():
        usuario.is_active = False
        usuario.deleted_at = ahora()
        usuario.save()
        messages.success(request, f"Usuario {usuario.username} archivado exitosamente.")
        return redirect(USUARIO_INDEX)

    return render(request, "backoffice/usuarios/usuario_delete.html", {
        "form": form,
        "usuario": usuario
    })


@login_required
@permission_required("users.view_usuario", raise_exception=True)
@require_safe
def trashcan_usuario(request):
    usuarios = Usuario.objects.filter(is_active=False)
    return render(request, "backoffice/usuarios/usuario_trashcan.html", {"usuarios": usuarios})


@login_required
@permission_required("users.change_usuario", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_usuario(request, pk):
    usuario = get_object_or_404(Usuario.objects, pk=pk, is_active=False)
    form = UsuarioRestoreForm(request.POST or None, usuario=usuario)

    if request.method == "POST" and form.is_valid():
        usuario.is_active = True
        usuario.deleted_at = None
        usuario.save()
        messages.success(request, f"Usuario {usuario.username} reincorporado exitosamente.")
        return redirect("users:usuario_trashcan")

    return render(request, "backoffice/usuarios/usuario_restore.html", {
        "form": form,
        "usuario": usuario
    })


@login_required
@permission_required("users.add_usuario", raise_exception=True)
def import_usuario(request):
    context = {
        'title': 'Importar Usuarios',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
    }
    return render(request, 'backoffice/usuarios/usuario_import.html', context)


@login_required
def perfil_usuario(request):
    if request.method == "POST":
        form = PerfilUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect("users:perfil")
    else:
        form = PerfilUpdateForm(instance=request.user)

    return render(request, "backoffice/usuarios/perfil.html", {"form": form})


# === GRUPOS ===
def filtrar_grupos(request, queryset=None):
    if queryset is None:
        queryset = Group.objects.all()

    nombre = request.GET.get("nombre")
    estado = request.GET.get("estado")

    if nombre:
        queryset = queryset.filter(name__icontains=nombre)

    if estado == "activo":
        queryset = queryset.filter(is_active=True)
    elif estado == "archivado":
        queryset = queryset.filter(is_active=False)

    return queryset


def generar_pdf_grupos(grupos, filtros, request):
    context = {
        'grupos': grupos,
        'filtros': filtros,
        'total_registros': grupos.count(),
        'usuario': request.user,
        'fecha_exportacion': ahora(),
    }
    html_string = render_to_string('backoffice/grupos/grupo_pdf.html', context)
    pdf = HTML(string=html_string).write_pdf()
    return pdf


@login_required
@permission_required("users.view_group", raise_exception=True)
@require_safe
def index_grupo(request):
    grupos = filtrar_grupos(request)

    if request.GET.get('export') == 'pdf':
        pdf = generar_pdf_grupos(grupos, request.GET, request)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = f"grupos_{ahora().strftime('%Y%m%d_%H%M%S')}.pdf"
        response['Content-Disposition'] = f'inline; filename={filename}'
        return response

    return render(request, "backoffice/grupos/grupo_index.html", {
        "grupos": grupos,
        "filtros": request.GET
    })


@login_required
@permission_required("users.add_group", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_grupo(request):
    form = GrupoCreateForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        grupo = form.save()
        messages.success(request, f"Grupo {grupo.name} creado exitosamente.")
        return redirect(GRUPO_INDEX)

    return render(request, "backoffice/grupos/grupo_create.html", {"form": form})


@login_required
@permission_required("users.change_group", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def update_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    form = GrupoUpdateForm(request.POST or None, instance=grupo)

    if request.method == "POST" and form.is_valid():
        grupo = form.save()
        messages.success(request, f"Grupo {grupo.name} actualizado exitosamente.")
        return redirect(GRUPO_INDEX)

    return render(request, "backoffice/grupos/grupo_update.html", {
        "form": form,
        "grupo": grupo
    })


@login_required
@permission_required("users.delete_group", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def delete_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk, is_active=True)
    form = GrupoDeleteForm(request.POST or None, grupo=grupo)

    if request.method == "POST" and form.is_valid():
        grupo.is_active = False
        grupo.save()
        messages.success(request, f"Grupo {grupo.name} archivado exitosamente.")
        return redirect(GRUPO_INDEX)

    return render(request, "backoffice/grupos/grupo_delete.html", {
        "form": form,
        "grupo": grupo
    })


@login_required
@permission_required("users.view_group", raise_exception=True)
@require_safe
def trashcan_grupo(request):
    grupos = Group.objects.filter(is_active=False)
    return render(request, "backoffice/grupos/grupo_trashcan.html", {"grupos": grupos})


@login_required
@permission_required("users.change_group", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def restore_grupo(request, pk):
    grupo = get_object_or_404(Group, pk=pk, is_active=False)
    form = GrupoRestoreForm(request.POST or None, grupo=grupo)

    if request.method == "POST" and form.is_valid():
        grupo.is_active = True
        grupo.save()
        messages.success(request, f"Grupo {grupo.name} reincorporado exitosamente.")
        return redirect("users:grupo_trashcan")

    return render(request, "backoffice/grupos/grupo_restore.html", {
        "form": form,
        "grupo": grupo
    })


@login_required
@permission_required("users.add_group", raise_exception=True)
def import_grupo(request):
    context = {
        'title': 'Importar Grupos',
        'subtitle': 'Carga masiva desde archivo CSV/Excel',
        'is_staff': request.user.is_staff,
        'datawizard_url': '/admin/sources/filesource/add/' if request.user.is_staff else None,
    }
    return render(request, 'backoffice/grupos/grupo_import.html', context)

#Metodo de actualizacion de perfil
def redirect_after_profile_update(user):
    if user.groups.filter(name='Clientes').exists():
        return redirect('guests:dashboard')
    else:
        return redirect('users:profile_update', pk=user.id)

@login_required
def update_usuario_auto(request, pk):
    if request.user.pk != pk:
        messages.error(request, "No puedes editar el perfil de otro usuario.")
        return redirect_after_profile_update(request.user)

    user = request.user
    
    if request.method == 'POST':
        profile_form = None
        password_form = None
        form_valid = False
        
        if 'update_profile' in request.POST:
            profile_form = ProfileUpdateForm(request.POST, instance=user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Perfil actualizado correctamente.")
                form_valid = True
            password_form = ChangePasswordForm(user)
            
        elif 'change_password' in request.POST:
            password_form = ChangePasswordForm(user, request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Contraseña actualizada correctamente.")
                form_valid = True
            profile_form = ProfileUpdateForm(instance=user)
        
        if form_valid:
            return redirect_after_profile_update(request.user)
            
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