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
    special_room = {
        'img': 'img/habitacionespecialHotel.webp',
        'titulo': 'Habitación Especial',
        'subtitulo': 'Confort exclusivo y lujo',
        'precio': '210.000',
        'precio_texto': 'noche',
        'btn_texto': 'Hacer Reserva'
    }
    
    regular_rooms = [
        {
            'img': 'img/habitacionbasicaHotel.webp',
            'titulo': 'Básica',
            'precio': '70.000'
        },
        {
            'img': 'img/habitacionfamiliarHotel.webp',
            'titulo': 'Familiar',
            'precio': '170.000'
        },
        {
            'img': 'img/habitacionparejaHotel.webp',
            'titulo': 'Pareja',
            'precio': '120.000'
        }
    ]
    
    promo_data = {
        'texto': '20% en tu primera reserva'
    }
    
    return render(request, 'hotel/habitaciones.html', {
        'special_room': special_room,
        'regular_rooms': regular_rooms,
        'promo_data': promo_data
    })

@require_GET
def restaurante(request):
    return render(request, "hotel/restaurante.html")

@require_GET
def signup(request):
    return render(request, "hotel/signup.html")

@require_GET
def login(request):
    return render(request, "hotel/login.html")
