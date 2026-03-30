from django.shortcuts import render
from django.views.decorators.http import require_GET,require_http_methods

@require_GET
def dashboard(request):
    return render(request,'backoffice/dashboard.html')

@require_GET
def create_reserva(request):
    #Por ahora vacia, se implementara despues
    pass

@require_GET
def index_reserva(request):
    #Por ahora vacia, se implementara despues
    pass