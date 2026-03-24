from django.shortcuts import render
from django.views.decorators.http import require_http_methods, require_POST, require_GET

# === IMPUESTO ===
@require_GET
def index_impuesto(request):
    return render(request,'backoffice/impuestos/impuesto_index.html')

@require_POST
def create_impuesto(request):
    return render(request,'backoffice/impuestos/impuesto_create.html')

@require_http_methods(['POST','GET'])
def update_impuesto(request):
    return render(request,'backoffice/impuestos/impuesto_update.html')

@require_http_methods(['POST','GET'])
def delete_impuesto(request):
    return render(request, 'backoffice/impuestos/impuesto_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_impuesto(request):
    return render(request,'backoffice/impuestos/impuesto_trashcan.html')

# === TARIFA ===
@require_GET
def index_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_index.html')

@require_POST
def create_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_create.html')

@require_http_methods(['POST','GET'])
def update_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_update.html')

@require_http_methods(['POST','GET'])
def delete_tarifa(request):
    return render(request, 'backoffice/tarifas/tarifa_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_tarifa(request):
    return render(request,'backoffice/tarifas/tarifa_trashcan.html')

# === TEMPORADA ===
@require_GET
def index_temporada(request):
    return render(request,'backoffice/temporadas/temporada_index.html')

@require_POST
def create_temporada(request):
    return render(request,'backoffice/temporada/temporada_create.html')

@require_http_methods(['POST','GET'])
def update_temporada(request):
    return render(request,'backoffice/temporadas/temporada_update.html')

@require_http_methods(['POST','GET'])
def delete_temporada(request):
    return render(request, 'backoffice/temporadas/temporada_delete.html')

@require_http_methods(['POST','GET'])
def trashcan_temporada(request):
    return render(request,'backoffice/temporadas/temporada_trashcan.html')