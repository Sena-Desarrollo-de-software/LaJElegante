{{-- resources/views/reservas/create.blade.php --}}
@extends('administrador.layouts.reservasr')

@section('title', 'Nueva Reserva')

@section('content')
<div class="container">
    <h1>Nueva Reserva</h1>

    <form action="{{ route('reservasr.gestion.store') }}" method="POST">
        @csrf

        <div class="mb-3">
            <label for="id_cliente" class="form-label">Cliente</label>
            <select name="id_cliente" id="id_cliente" class="form-control" required>
                <option value="">Seleccione un cliente</option>
                @foreach($clientes as $cliente)
                    <option value="{{ $cliente->id_cliente }}">
                        {{ $cliente->nombre }} {{ $cliente->apellido }}
                    </option>
                @endforeach
            </select>
        </div>

        <div class="mb-3">
            <label for="id_mesa" class="form-label">Mesa</label>
            <select name="id_mesa" id="id_mesa" class="form-control" required>
                <option value="">Seleccione una mesa</option>
                @foreach($mesas as $mesa)
                    <option value="{{ $mesa->id_mesa }}">
                        Mesa {{ $mesa->numero_mesa }} (Capacidad: {{ $mesa->capacidad }})
                    </option>
                @endforeach
            </select>
        </div>

        <div class="mb-3">
            <label for="fecha_reserva" class="form-label">Fecha</label>
            <input type="date" name="fecha_reserva" id="fecha_reserva" class="form-control" required>
        </div>

        <div class="mb-3">
            <label for="hora_reserva" class="form-label">Hora</label>
            <input type="time" name="hora_reserva" id="hora_reserva" class="form-control" required>
        </div>

        <div class="mb-3">
            <label for="numero_personas" class="form-label">Número de Personas</label>
            <input type="number" name="numero_personas" id="numero_personas" class="form-control" min="1" required>
        </div>

        <div class="mb-3">
            <label for="estado_reserva" class="form-label">Estado</label>
            <select name="estado_reserva" id="estado_reserva" class="form-control" required>
                <option value="pendiente">Pendiente</option>
                <option value="confirmada">Confirmada</option>
                <option value="cancelada">Cancelada</option>
            </select>
        </div>

        <div class="mb-3">
            <label for="activo" class="form-label">Activo</label>
            <select name="activo" id="activo" class="form-control" required>
                <option value="1" selected>Sí</option>
                <option value="0">No</option>
            </select>
        </div>

        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{{ route('reservasr.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection