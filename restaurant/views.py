from django.shortcuts import render
from django.views.decorators.http import require_GET,require_POST,require_http_methods

# === HORARIO ===
@require_GET
def index_horario(request):
    return render(request,'backoffice/horarios/horario_index.html')

@require_POST
def create_horario(request):
    return render(request,'backoffice/horarios/horario_create.html')

@require_http_methods(['POST','GET'])
def update_horario(request):
    return render(request,'backoffice/horarios/horario_update.html')

@require_http_methods(['POST','GET'])
def delete_horario(request):
    return render(request, 'backoffice/horarios/horario_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_horario(request):
    return render(request,'backoffice/horarios/horario_trashcan.html')

# === MESA ===
@require_GET
def index_mesa(request):
    return render(request,'backoffice/horarios/mesa_index.html')

@require_POST
def create_mesa(request):
    return render(request,'backoffice/horarios/mesa_create.html')

@require_http_methods(['POST','GET'])
def update_mesa(request):
    return render(request,'backoffice/horarios/mesa_update.html')

@require_http_methods(['POST','GET'])
def delete_mesa(request):
    return render(request, 'backoffice/horarios/mesa_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_mesa(request):
    return render(request,'backoffice/horarios/mesa_trashcan.html')

# === RESERVA RESTAURANTE ===
@require_GET
def index_reserva_restaurante(request):
    return render(request,'backoffice/horarios/reserva_restaurante_index.html')

@require_POST
def create_reserva_restaurante(request):
    return render(request,'backoffice/horarios/reserva_restaurante_create.html')

@require_http_methods(['POST','GET'])
def update_reserva_restaurante(request):
    return render(request,'backoffice/horarios/reserva_restaurante_update.html')

@require_http_methods(['POST','GET'])
def delete_reserva_restaurante(request):
    return render(request, 'backoffice/horarios/reserva_restaurante_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_reserva_restaurante(request):
    return render(request,'backoffice/horarios/reserva_restaurante_trashcan.html')