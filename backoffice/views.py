from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_GET,require_http_methods
from .models import DashboardService
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_http_methods, require_POST, require_safe, require_GET
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .forms import ReservaCreateForm
from core.models import Reserva
from users.models import Usuario

@require_GET
def dashboard(request):
    querys = DashboardService.get_dashboard_for_user(request.user)
    return render(request,'backoffice/dashboard.html', {'dashboard' : querys})

@login_required
@permission_required("core.create_reserva", raise_exception=True)
@require_http_methods(["GET", "POST"])
@csrf_protect
def create_reserva(request):
    form = ReservaCreateForm(request.POST or None)
    next_view = request.GET.get("next") or request.POST.get("next")

    if request.method == "POST" and form.is_valid():
        reserva = form.save(user=request.user)
        if next_view == "reserva_habitacion":
            return redirect("rooms:reserva_habitacion_create", reserva_id=reserva.id)
        return redirect("backoffice:reserva_detail", reserva.id)
    return render(request, "backoffice/reservas/reserva_create.html", {
        "form": form
    })

@login_required
@permission_required("core.view_reserva", raise_exception=True)
def detail_reserva(request, pk):
    reserva = get_object_or_404(Reserva, pk=pk)

    return render(request, "backoffice/reservas/reserva_detail.html", {
        "reserva": reserva
    })

@login_required
@permission_required("core.view_reserva", raise_exception=True)
@require_safe
def index_reserva(request):
    reservas = Reserva.objects.select_related("usuario").all().order_by("-id")

    usuario = request.GET.get("usuario")
    estado = request.GET.get("estado")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    if usuario:
        reservas = reservas.filter(usuario__id=usuario)

    if estado:
        reservas = reservas.filter(estado=estado)

    if fecha_inicio:
        reservas = reservas.filter(fecha_reserva__date__gte=fecha_inicio)

    if fecha_fin:
        reservas = reservas.filter(fecha_reserva__date__lte=fecha_fin)

    usuarios = Usuario.objects.all()

    return render(request, "backoffice/reservas/reserva_index.html", {
        "reservas": reservas,
        "usuarios": usuarios,
        "filtros": request.GET
    })