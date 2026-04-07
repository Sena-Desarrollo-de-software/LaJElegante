# Vista protegida para reservar habitación
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def reservar_habitacion(request):
    return HttpResponse('<h1>Reserva de habitación: solo usuarios autenticados pueden ver esto.</h1>')
from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_GET,require_http_methods
from .models import Promocion
from django.utils import timezone
from .forms import RegistroForm
from users.models import Group
from django.urls import reverse_lazy
from django.conf import settings
import requests
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from django.core.cache import cache
import random

AHORA = timezone.now()

PROMOCIONES_NAV = Promocion.objects.filter(
    estado='PUBLICADO',
    tipo__in=['NAVBAR','AMBOS'],
    orden_navbar__isnull=False,
    fecha_inicio__lte=AHORA,
    fecha_fin__gte=AHORA,
).order_by('orden_navbar')

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

    return render(request, "hotel/lobby.html", {'carousel_items': carousel_items, 'promos' : PROMOCIONES_NAV})

@require_GET
def tyc(request):
    return render(request, "hotel/tyc.html",{'promos' : PROMOCIONES_NAV})

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
        'promo_data': promo_data,
        'promos' : PROMOCIONES_NAV
    })

@require_GET
def restaurante(request):
    disponibilidad_data = {
        'titulo': 'Mesas disponibles para hoy',
        'subtitulo': 'Consulta en tiempo real la disponibilidad',
        'contador': '--#--'
    }
    
    boton_data = {
        'texto': '¡Reservar ahora!',
        'url': '#'
    }
    
    platos_list = [
        {
            'img': 'img/plato1.webp',
            'nombre': 'Ajiaco Santafereño',
            'precio': '23.000'
        },
        {
            'img': 'img/plato2.webp',
            'nombre': 'Corrientazo del día',
            'precio': '20.500'
        }
    ]
    
    return render(request, 'hotel/restaurante.html', {
        'disponibilidad_data': disponibilidad_data,
        'boton_data': boton_data,
        'platos_list': platos_list,
        'promos' : PROMOCIONES_NAV
    })

@require_GET
def promociones(request):
    promociones_nav_lp = Promocion.objects.filter(
        estado='PUBLICADO',
        tipo__in=['PAGINA','AMBOS'],
        orden_navbar__isnull=False,
        fecha_inicio__lte=AHORA,
        fecha_fin__gte=AHORA,
    ).order_by('orden_navbar')
    return render(request, "hotel/promociones.html",{"promociones_nav" : promociones_nav_lp,'promos' : PROMOCIONES_NAV})

@login_required
def mi_panel(request):
    if request.user.groups.filter(name__in=['Cliente', 'Clientes']).exists():
        return redirect('guests:dashboard')
    return redirect('backoffice:dashboard')

class LoginUsuario(LoginView):
    template_name = 'hotel/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promos'] = PROMOCIONES_NAV
        return context
    
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name__in=['Cliente', 'Clientes']).exists():
            return reverse_lazy('guests:dashboard')
        return reverse_lazy('backoffice:dashboard')

class RegistroUsuario(CreateView):
    form_class = RegistroForm
    template_name = 'hotel/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promos'] = PROMOCIONES_NAV
        return context
    
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name__in=['Cliente', 'Clientes']).exists():
            return reverse_lazy('guests:dashboard')
        return reverse_lazy('backoffice:dashboard')

    def form_valid(self, form):
        user = form.save()

        grupo, _ = Group.objects.get_or_create(name='Clientes')
        user.groups.add(grupo)

        login(self.request, user)

        return redirect(self.get_success_url())
        
class LogoutUsuario(LogoutView):
    next_page = 'login'
    http_method_names = ['get', 'post', 'options']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class CustomPasswordResetView(PasswordResetView):
    template_name = 'hotel/password_reset.html'
    email_template_name = 'hotel/password_reset_email.txt'
    html_email_template_name = 'hotel/password_reset_email.html'
    subject_template_name = 'hotel/components/auth/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['domain'] = '127.0.0.1:8000'
        context['protocol'] = 'http'
        return context

    def get_from_email(self):
        return settings.FROM_EMAILS['ayuda']
    
class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'hotel/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'hotel/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'hotel/password_reset_complete.html'

import requests
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import random

@cache_page(60 * 15)
def tienda_hotel(request):
    categorias_config = {
        'beauty': {
            'nombre': '💆‍♀️ Spa & Bienestar',
            'descripcion': 'Productos de nuestros tratamientos de spa',
            'icono': 'bi-flower2',
            'limit': 4
        },
        'fragrances': {
            'nombre': '👃 Perfumes Exclusivos',
            'descripcion': 'Fragancias que ambientan nuestro hotel',
            'icono': 'bi-gem',
            'limit': 4
        },
        'home-decoration': {
            'nombre': '🛋️ Decoración Hotelera',
            'descripcion': 'Piezas únicas de nuestras habitaciones',
            'icono': 'bi-house-heart',
            'limit': 4
        },
        'groceries': {
            'nombre': '🍷 Delicias Gourmet',
            'descripcion': 'Productos de nuestro restaurante',
            'icono': 'bi-cup-straw',
            'limit': 4
        }
    }
    
    productos_por_categoria = {}
    todas_categorias = []
    
    for categoria, config in categorias_config.items():
        try:
            url = f"https://dummyjson.com/products/category/{categoria}?limit={config['limit']}"
            response = requests.get(url, timeout=5)
            data = response.json()
            
            productos = []
            for producto in data.get('products', []):
                producto_hotel = {
                    'id': producto['id'],
                    'nombre': f"{producto['title']} - Hotel LJE",
                    'descripcion': f"Exclusivo Hotel LJE. {producto['description'][:100]}...",
                    'precio_hotel': round(producto['price'] * 1.3, 2),
                    'precio_original': producto['price'],
                    'descuento': producto['discountPercentage'],
                    'imagen': producto['thumbnail'],
                    'disponible': producto['availabilityStatus'] == 'In Stock',
                }
                productos.append(producto_hotel)
                todas_categorias.append(producto_hotel)
            
            productos_por_categoria[categoria] = {
                'config': config,
                'productos': productos
            }
        except:
            productos_por_categoria[categoria] = {
                'config': config,
                'productos': []
            }
    
    promociones = random.sample(todas_categorias, min(3, len(todas_categorias))) if todas_categorias else []
    
    return render(request, 'hotel/tienda_souvenirs.html', {
        'productos_por_categoria': productos_por_categoria,
        'promociones': promociones,
        'fecha_actualizacion': timezone.now()
    })