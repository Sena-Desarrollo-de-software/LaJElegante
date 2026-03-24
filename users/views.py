from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST, require_GET

# === USUARIO ===
@require_GET
def index_usuario(request):
    return render(request,'backoffice/usuario/usuario_index.html')

@require_POST
def create_usuario(request):
    return render(request,'backoffice/usuario/usuario_create.html')

@require_http_methods(['POST','GET'])
def update_usuario(request):
    return render(request,'backoffice/usuario/usuario_update.html')

@require_http_methods(['POST','GET'])
def delete_usuario(request):
    return render(request, 'backoffice/usuario/usuario_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_usuario(request):
    return render(request,'backoffice/usuario/usuario_trashcan.html')

# === GRUPO ===
@require_GET
def index_grupo(request):
    return render(request,'backoffice/grupo/grupo_index.html')

@require_POST
def create_grupo(request):
    return render(request,'backoffice/grupo/grupo_create.html')

@require_http_methods(['POST','GET'])
def update_grupo(request):
    return render(request,'backoffice/grupo/grupo_update.html')

@require_http_methods(['POST','GET'])
def delete_grupo(request):
    return render(request, 'backoffice/grupo/grupo_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_grupo(request):
    return render(request,'backoffice/grupo/grupo_trashcan.html')