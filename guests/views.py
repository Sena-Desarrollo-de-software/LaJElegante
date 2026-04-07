from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from backoffice.forms import ReservaCreateForm
from core.models import Reserva
from finance.models import Tarifa
from restaurant.models import Horario, Turno, ReservaRestaurante
from rooms.models import ReservaHabitacion, TipoHabitacion
from users.forms import ProfileUpdateForm, ChangePasswordForm

from .forms import (
    GuestReservaHabitacionCreateForm,
    GuestReservaHabitacionUpdateForm,
    GuestReservaRestauranteForm,
)


def _es_cliente(user):
    return user.groups.filter(name__in=['Cliente', 'Clientes']).exists()


def _validar_cliente(user):
    if not _es_cliente(user):
        raise PermissionDenied


def _cancelar_reserva_completa(reserva):
    errores = []
    turnos_afectados_ids = set()

    for reserva_habitacion in reserva.reserva_habitaciones.filter(is_active=True):
        if reserva_habitacion.estado != 'CANCELADA':
            try:
                reserva_habitacion.cancelar()
            except ValidationError as exc:
                errores.extend(exc.messages if hasattr(exc, 'messages') else [str(exc)])

    for reserva_restaurante in reserva.reserva_restaurantes.select_related('turno').filter(is_active=True):
        if reserva_restaurante.turno_id:
            turnos_afectados_ids.add(reserva_restaurante.turno_id)
        if reserva_restaurante.estado != 'CANCELADA':
            try:
                reserva_restaurante.cancelar()
            except ValidationError as exc:
                errores.extend(exc.messages if hasattr(exc, 'messages') else [str(exc)])

    if turnos_afectados_ids:
        for turno in Turno.objects.filter(pk__in=turnos_afectados_ids):
            turno.recalcular_quorum()

    if errores:
        return False, errores

    reserva.estado = 'CANCELADA'
    reserva.save(update_fields=['estado', 'updated_at'])
    return True, []


@login_required
def dashboard(request):
    _validar_cliente(request.user)
    reservas = Reserva.objects.filter(usuario=request.user).order_by('-id')[:3]
    stats = {
        'total': Reserva.objects.filter(usuario=request.user).count(),
        'pendiente': Reserva.objects.filter(usuario=request.user, estado='PENDIENTE').count(),
        'confirmada': Reserva.objects.filter(usuario=request.user, estado='CONFIRMADA').count(),
        'cancelada': Reserva.objects.filter(usuario=request.user, estado='CANCELADA').count(),
    }
    return render(request, 'guests/dashboard.html', {'reservas': reservas, 'stats': stats})


@login_required
def perfil(request):
    _validar_cliente(request.user)
    user = request.user

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            form = ProfileUpdateForm(request.POST, instance=user)
            password_form = ChangePasswordForm(user)

            if form.is_valid():
                form.save()
                messages.success(request, 'Perfil actualizado correctamente.')
                return redirect('guests:perfil')

        elif 'change_password' in request.POST:
            form = ProfileUpdateForm(instance=user)
            password_form = ChangePasswordForm(user, request.POST)

            if password_form.is_valid():
                password_form.save()
                messages.success(request, 'Contraseña actualizada correctamente.')
                return redirect('login')
        else:
            form = ProfileUpdateForm(instance=user)
            password_form = ChangePasswordForm(user)
    else:
        form = ProfileUpdateForm(instance=user)
        password_form = ChangePasswordForm(user)

    return render(request, 'guests/perfil.html', {
        'form': form,
        'password_form': password_form,
    })


@login_required
def reserva_habitacion_list(request):
    _validar_cliente(request.user)
    reservas = ReservaHabitacion.objects.filter(reserva__usuario=request.user, is_active=True).select_related('habitacion', 'reserva').order_by('-id')
    return render(request, 'guests/reserva_habitacion_list.html', {'reservas': reservas})


@login_required
def reserva_habitacion_create(request):
    _validar_cliente(request.user)
    post_data = request.POST or None
    if request.method == 'POST' and request.POST.get('vivienda') and not request.POST.get('habitacion'):
        post_data = request.POST.copy()
        post_data['habitacion'] = request.POST.get('vivienda')

    fecha_inicio = request.GET.get('fecha_inicio') or (post_data.get('fecha_inicio') if post_data else None)
    fecha_fin = request.GET.get('fecha_fin') or (post_data.get('fecha_fin') if post_data else None)

    form = GuestReservaHabitacionCreateForm(
        post_data,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    if request.method == 'POST' and form.is_valid():
        reserva = Reserva.objects.create(
            usuario=request.user,
            estado='PENDIENTE',
            created_by=request.user,
            updated_by=request.user,
        )
        item = form.save(commit=False)
        item.reserva = reserva
        item.descuento = 0
        item.created_by = request.user
        item.updated_by = request.user
        item.save()
        messages.success(request, 'Reserva de habitación creada correctamente.')
        return redirect('guests:reserva_habitacion_list')

    return render(request, 'guests/reserva_habitacion_form.html', {'form': form, 'modo': 'crear'})


@login_required
def reserva_habitacion_update(request, pk):
    _validar_cliente(request.user)
    reserva = get_object_or_404(ReservaHabitacion, pk=pk, reserva__usuario=request.user)
    if reserva.estado == 'CANCELADA' or reserva.reserva.estado == 'CANCELADA':
        messages.error(request, 'No se puede editar una reserva cancelada.')
        return redirect('guests:reserva_habitacion_list')

    form = GuestReservaHabitacionUpdateForm(request.POST or None, instance=reserva)

    if request.method == 'POST' and form.is_valid():
        item = form.save(commit=False)
        item.descuento = 0
        item.updated_by = request.user
        item.save()
        messages.success(request, 'Reserva de habitación actualizada correctamente.')
        return redirect('guests:reserva_habitacion_list')

    return render(request, 'guests/reserva_habitacion_form.html', {'form': form, 'modo': 'editar'})


@login_required
def reserva_habitacion_cancel(request, pk):
    _validar_cliente(request.user)
    if request.method != 'POST':
        messages.error(request, 'La cancelación debe enviarse por formulario.')
        return redirect('guests:reserva_habitacion_list')

    reserva_habitacion = get_object_or_404(ReservaHabitacion, pk=pk, reserva__usuario=request.user)
    with transaction.atomic():
        ok, errores = _cancelar_reserva_completa(reserva_habitacion.reserva)
    if ok:
        messages.success(request, 'Reserva cancelada correctamente.')
    else:
        for error in errores:
            messages.error(request, error)
    return redirect('guests:reserva_habitacion_list')


@login_required
def reserva_cancel(request, pk):
    _validar_cliente(request.user)
    if request.method != 'POST':
        messages.error(request, 'La cancelación debe enviarse por formulario.')
        return redirect('guests:dashboard')

    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    with transaction.atomic():
        ok, errores = _cancelar_reserva_completa(reserva)

    if ok:
        messages.success(request, 'Reserva cancelada correctamente.')
    else:
        for error in errores:
            messages.error(request, error)
    return redirect('guests:dashboard')


@login_required
def reserva_detail(request, pk):
    _validar_cliente(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)
    habitaciones = reserva.reserva_habitaciones.select_related('habitacion').filter(is_active=True)
    restaurantes = reserva.reserva_restaurantes.select_related('turno', 'turno__horario').filter(is_active=True)
    tiene_habitaciones = habitaciones.exists()
    tiene_restaurantes = restaurantes.exists()
    return render(
        request,
        'guests/reserva_detail.html',
        {
            'reserva': reserva,
            'habitaciones': habitaciones,
            'restaurantes': restaurantes,
            'tiene_habitaciones': tiene_habitaciones,
            'tiene_restaurantes': tiene_restaurantes,
        },
    )


@login_required
def reserva_edit(request, pk):
    _validar_cliente(request.user)
    reserva = get_object_or_404(Reserva, pk=pk, usuario=request.user)

    if reserva.estado == 'CANCELADA':
        messages.error(request, 'No se puede editar una reserva cancelada.')
        return redirect('guests:dashboard')

    reserva_habitacion = reserva.reserva_habitaciones.exclude(estado='CANCELADA').order_by('-id').first()
    if reserva_habitacion:
        return redirect('guests:reserva_habitacion_update', pk=reserva_habitacion.pk)

    reserva_restaurante = reserva.reserva_restaurantes.exclude(estado='CANCELADA').order_by('-id').first()
    if reserva_restaurante:
        return redirect('guests:reserva_restaurante_update', pk=reserva_restaurante.pk)

    messages.error(request, 'No hay servicios editables en esta reserva.')
    return redirect('guests:reserva_detail', pk=reserva.pk)


@login_required
def reserva_restaurante_list(request):
    _validar_cliente(request.user)
    reservas = ReservaRestaurante.objects.filter(reserva__usuario=request.user, is_active=True).select_related('turno', 'turno__horario', 'reserva').order_by('-id')
    return render(request, 'guests/reserva_restaurante_list.html', {'reservas': reservas})


@login_required
def reserva_restaurante_create(request):
    _validar_cliente(request.user)
    form_kwargs = {}
    if request.method == 'GET':
        fecha = request.GET.get('fecha')
        if fecha:
            form_kwargs['initial'] = {'fecha': fecha}

    form = GuestReservaRestauranteForm(request.POST or None, **form_kwargs)

    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                reserva = Reserva.objects.create(
                    usuario=request.user,
                    estado='PENDIENTE',
                    created_by=request.user,
                    updated_by=request.user,
                )
                item = form.save(commit=False)
                item.reserva = reserva
                item.descuento = 0
                item.created_by = request.user
                item.updated_by = request.user
                item.save()
            messages.success(request, 'Reserva de restaurante creada correctamente.')
            return redirect('guests:reserva_restaurante_list')
        except ValidationError as exc:
            errores = exc.messages if hasattr(exc, 'messages') else [str(exc)]
            for error in errores:
                messages.error(request, error)

    return render(request, 'guests/reserva_restaurante_form.html', {'form': form, 'modo': 'crear'})


@login_required
def reserva_restaurante_update(request, pk):
    _validar_cliente(request.user)
    reserva = get_object_or_404(ReservaRestaurante, pk=pk, reserva__usuario=request.user)
    if reserva.estado == 'CANCELADA' or reserva.reserva.estado == 'CANCELADA':
        messages.error(request, 'No se puede editar una reserva cancelada.')
        return redirect('guests:reserva_restaurante_list')

    form = GuestReservaRestauranteForm(request.POST or None, instance=reserva)

    if request.method == 'POST' and form.is_valid():
        try:
            item = form.save(commit=False)
            item.descuento = 0
            item.updated_by = request.user
            item.save()
            messages.success(request, 'Reserva de restaurante actualizada correctamente.')
            return redirect('guests:reserva_restaurante_list')
        except ValidationError as exc:
            errores = exc.messages if hasattr(exc, 'messages') else [str(exc)]
            for error in errores:
                messages.error(request, error)

    return render(request, 'guests/reserva_restaurante_form.html', {'form': form, 'modo': 'editar'})


@login_required
def reserva_restaurante_cancel(request, pk):
    _validar_cliente(request.user)
    if request.method != 'POST':
        messages.error(request, 'La cancelación debe enviarse por formulario.')
        return redirect('guests:reserva_restaurante_list')

    reserva_restaurante = get_object_or_404(ReservaRestaurante, pk=pk, reserva__usuario=request.user)
    with transaction.atomic():
        ok, errores = _cancelar_reserva_completa(reserva_restaurante.reserva)

    if ok:
        messages.success(request, 'Reserva cancelada correctamente.')
    else:
        for error in errores:
            messages.error(request, error)
    return redirect('guests:reserva_restaurante_list')


@login_required
def tarifas_list(request):
    _validar_cliente(request.user)
    tarifas = Tarifa.objects.select_related('temporada', 'servicio_tipo').order_by('-id')
    return render(request, 'guests/tarifas_list.html', {'tarifas': tarifas})


@login_required
def tipos_habitacion_list(request):
    _validar_cliente(request.user)
    tipos = TipoHabitacion.objects.all().order_by('nombre_tipo')
    return render(request, 'guests/tipos_habitacion_list.html', {'tipos': tipos})


@login_required
def horarios_list(request):
    _validar_cliente(request.user)
    horarios = Horario.objects.all().order_by('hora_inicio')
    return render(request, 'guests/horarios_list.html', {'horarios': horarios})


@login_required
def turnos_list(request):
    _validar_cliente(request.user)
    turnos = Turno.objects.select_related('horario').order_by('fecha', 'horario__hora_inicio')
    return render(request, 'guests/turnos_list.html', {'turnos': turnos})
