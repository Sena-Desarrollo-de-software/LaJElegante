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
def index_turno(request):
    return render(request,'backoffice/turnos/turno_index.html')

@require_POST
def create_turno(request):
    return render(request,'backoffice/turnos/turno_create.html')

@require_http_methods(['POST','GET'])
def update_turno(request):
    return render(request,'backoffice/turnos/turno_update.html')

@require_http_methods(['POST','GET'])
def delete_turno(request):
    return render(request, 'backoffice/turnos/turno_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_turno(request):
    return render(request,'backoffice/turnos/turno_trashcan.html')

# === RESERVA RESTAURANTE ===
@require_GET
def index_reserva_restaurante(request):
    return render(request,'backoffice/reservas_restaurante/reserva_restaurante_index.html')

@require_POST
def create_reserva_restaurante(request):
    return render(request,'backoffice/reservas_restaurante/reserva_restaurante_create.html')

@require_http_methods(['POST','GET'])
def update_reserva_restaurante(request):
    return render(request,'backoffice/reservas_restaurante/reserva_restaurante_update.html')

@require_http_methods(['POST','GET'])
def delete_reserva_restaurante(request):
    return render(request, 'backoffice/reservas_restaurante/reserva_restaurante_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_reserva_restaurante(request):
    return render(request,'backoffice/reservas_restaurante/reserva_restaurante_trashcan.html')