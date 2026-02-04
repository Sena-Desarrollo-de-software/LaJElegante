{{-- resources/views/reservas/show.blade.php --}}
@extends('administrador.layouts.reservasr')

@section('title', 'Detalle de Reserva')

@section('content')
    <h1>Detalle de la Reserva</h1>

    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Reserva #{{ $reserva->id_reserva }}</h5>

            <p><strong>Cliente:</strong> {{ $reserva->cliente->nombre ?? 'Sin asignar' }}</p>
            <p><strong>Mesa:</strong> {{ $reserva->mesa->numero_mesa ?? 'Sin asignar' }}</p>
            <p><strong>Fecha:</strong> {{ $reserva->fecha_reserva }}</p>
            <p><strong>Hora:</strong> {{ $reserva->hora_reserva }}</p>
            <p><strong>Número de Personas:</strong> {{ $reserva->numero_personas }}</p>
            <p><strong>Estado:</strong> {{ $reserva->estado_reserva }}</p>
            <p><strong>Activo:</strong> {{ $reserva->activo ? 'Sí' : 'No' }}</p>
        </div>
    </div>

    <a href="{{ route('reservasr.gestion.index') }}" class="btn btn-secondary mt-3">Volver al listado</a>
    <a href="{{ route('reservasr.gestion.edit', $reserva->id_reserva) }}" class="btn btn-warning mt-3">Editar</a>
@endsection
