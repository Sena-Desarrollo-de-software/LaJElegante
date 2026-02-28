from django.shortcuts import render
from django.views.decorators.http import require_GET,require_http_methods

@require_GET
def lobby(request):
    carousel_items = [
        {
            'img': 'img/hotel2.webp',
            'titulo': 'Bienvenido al Hotel La J Elegante',
            'descripcion': 'Tu descanso y confort en un solo lugar',
            'active': True
        },
        {
            'img': 'img/restauranteHotel2.webp',
            'titulo': 'Experiencias únicas',
            'descripcion': 'Restaurante gourmet y servicio exclusivo',
            'active': False
        },
        {
            'img': 'img/fondologinHotel.webp',
            'titulo': 'Relájate en nuestras habitaciones',
            'descripcion': 'Comodidad y estilo al alcance de tu mano',
            'active': False
        },
    ]
    
    return render(request, "hotel/lobby.html", {'carousel_items': carousel_items})

@require_GET
def tyc(request):
    return render(request, "tyc/lobby.html")

@require_GET
def habitaciones(request):
    return render(request, "hotel/habitaciones.html")

@require_GET
def restaurante(request):
    return render(request, "hotel/restaurante.html")

@require_GET
def signup(request):
    return render(request, "hotel/signup.html")

@require_GET
def login(request):
    return render(request, "hotel/login.html")
