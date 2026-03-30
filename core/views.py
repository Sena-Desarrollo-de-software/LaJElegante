from django.shortcuts import render,redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_GET,require_http_methods
from .models import Promocion
from users.models import Group
from .forms import RegistroForm
from django.utils import timezone
from django.urls import reverse_lazy

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

class LoginUsuario(LoginView):
    template_name = 'hotel/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promos'] = PROMOCIONES_NAV
        return context
    
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Cliente').exists():
            return reverse_lazy('clientes:home')
        return reverse_lazy('backoffice:dashboard')

class RegistroUsuario(CreateView):
    form_class = RegistroForm
    template_name = 'hotel/signup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['promos'] = PROMOCIONES_NAV
        return context
    
    def get_success_url(self):
        return reverse_lazy('backoffice:dashboard')

    def form_valid(self, form):
        user = form.save()

        grupo, _ = Group.objects.get_or_create(name='Clientes')
        user.groups.add(grupo)

        login(self.request, user)

        return redirect(self.get_success_url())
        
class LogoutUsuario(LogoutView):
    next_page = 'login'