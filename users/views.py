from django.shortcuts import render,redirect
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_GET,require_http_methods
from core.views import PROMOCIONES_NAV
from .models import Group
from .forms import RegistroForm
from django.urls import reverse_lazy

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