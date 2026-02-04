@extends('administrador.layouts.reservash')

@section('content')
<h2 class="mb-4">Nueva Reserva</h2>

<form action="{{ route('reservash.gestion.store') }}" method="POST">
    @csrf

    <div class="mb-3">
        <label for="id_cliente" class="form-label">Cliente</label>
        <select name="id_cliente" class="form-select" required>
            <option value="">Seleccione un cliente</option>
            @foreach($clientes as $cliente)
                <option value="{{ $cliente->id_cliente }}">{{ $cliente->nombre }}</option>
            @endforeach
        </select>
    </div>

    <div class="mb-3">
        <label for="id_habitacion" class="form-label">Habitación</label>
        <select name="id_habitacion" id="habitacion-select" class="form-select" data-tarifa-url="{{ route('tarifas.porHabitacion', ['habitacion' => ':id']) }}" required>
            <option value="">Seleccione una habitación</option>
            @foreach($habitaciones as $habitacion)
                <option value="{{ $habitacion->id_habitacion }}">Habitación {{ $habitacion->numero_habitacion }}</option>
            @endforeach
        </select>
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label class="form-label">Fecha Inicio</label>
            <input type="date" name="fecha_inicio" id="fecha_inicio" class="form-control" required min="{{ date('Y-m-d') }}">
        </div>
        <div class="col-md-6 mb-3">
            <label class="form-label">Fecha Fin</label>
            <input type="date" name="fecha_fin" id="fecha_fin" class="form-control" required>
        </div>
    </div>

    <div class="row">
        <div class="col-md-4 mb-3">
            <label class="form-label">Personas</label>
            <input type="number" name="cantidad_personas" class="form-control" min="1" required>
            <small id="aviso-capacidad" class="form-text text-muted"></small>
        </div>
        <div class="col-md-4 mb-3">
            <label class="form-label">Noches</label>
            <input type="number" name="noches" class="form-control" min="1" readonly>
        </div>
        <div class="col-md-4 mb-3">
            <label class="form-label">Precio por Noche</label>
            <input type="number" name="precio_noche" class="form-control" readonly>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label class="form-label">Descuento (%)</label>
            <input type="number" step="1" name="descuento_aplicado" class="form-control" value="0">
        </div>
        <div class="col-md-6 mb-3">
            <label class="form-label">Recargo (%)</label>
            <input type="number" step="1" name="recargo_aplicado" class="form-control" value="0">
        </div>
    </div>

    <div class="mb-3">
        <label class="form-label">Precio Total</label>
        <input type="number" name="precio_reserva" id="precio_reserva" class="form-control" readonly>
    </div>

    <div class="mb-3">
        <label class="form-label">Observaciones</label>
        <textarea name="observaciones" class="form-control"></textarea>
    </div>

    <button type="submit" class="btn btn-success">Guardar</button>
    <a href="{{ route('reservash.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
</form>
@endsection

@push('scripts')
    <script src="{{ asset('build/assets/js/reservas.js') }}"></script>
@endpush