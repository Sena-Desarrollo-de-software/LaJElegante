from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.views.decorators.http import require_GET,require_http_methods

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

def update_usuario_auto(request):
    return(request,'backoffice/profile/profile_edit.html')