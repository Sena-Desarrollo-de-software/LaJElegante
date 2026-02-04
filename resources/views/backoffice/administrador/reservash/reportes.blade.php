@extends('administrador.layouts.reservash')

@section('content')
<div class="container">
    <h1 class="mb-4">Reportes de Reservas de Habitaciones</h1>

    <form method="GET" action="{{ route('reservash.reportes') }}" class="row g-3 mb-4">
        <div class="col-md-3">
            <label for="tipo" class="form-label">Tipo de Cliente</label>
            <select name="tipo" id="tipo" class="form-select">
                <option value="">Todos</option>
                @foreach ($tipos as $t)
                    <option value="{{ $t->id_tipo_cliente }}" {{ request('tipo') == $t->id_tipo_cliente ? 'selected' : '' }}>
                        {{ $t->nombre_tipo }}
                    </option>
                @endforeach
            </select>
        </div>

        <div class="col-md-3">
            <label for="desde" class="form-label">Desde</label>
            <input type="date" name="desde" id="desde" value="{{ request('desde') }}" class="form-control">
        </div>

        <div class="col-md-3">
            <label for="hasta" class="form-label">Hasta</label>
            <input type="date" name="hasta" id="hasta" value="{{ request('hasta') }}" class="form-control">
        </div>

        <div class="col-md-3">
            <label for="noches_min" class="form-label">Noches (mín.)</label>
            <input type="number" name="noches_min" id="noches_min" value="{{ request('noches_min') }}" class="form-control">
        </div>

        <div class="col-md-3">
            <label for="noches_max" class="form-label">Noches (máx.)</label>
            <input type="number" name="noches_max" id="noches_max" value="{{ request('noches_max') }}" class="form-control">
        </div>

        <div class="col-md-3">
            <label for="personas_min" class="form-label">Personas (mín.)</label>
            <input type="number" name="personas_min" id="personas_min" value="{{ request('personas_min') }}" class="form-control">
        </div>

        <div class="col-md-3">
            <label for="personas_max" class="form-label">Personas (máx.)</label>
            <input type="number" name="personas_max" id="personas_max" value="{{ request('personas_max') }}" class="form-control">
        </div>

        <div class="col-md-3 d-flex align-items-end">
            <button type="submit" class="btn btn-primary w-100">Filtrar</button>
        </div>
    </form>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>Cliente</th>
                <th>Habitación</th>
                <th>Fechas</th>
                <th>Noches</th>
                <th>Precio Total</th>
                <th>Observaciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($reservas as $r)
                <tr>
                    <td>{{ $r->cliente->nombre }} {{ $r->cliente->apellido }}</td>
                    <td>{{ $r->detalle->habitacion->numero_habitacion }}</td>
                    <td>{{ $r->detalle->fecha_inicio }} - {{ $r->detalle->fecha_fin }}</td>
                    <td>{{ $r->detalle->noches }}</td>
                    <td>${{ number_format($r->detalle->precio_reserva, 2) }}</td>
                    <td>{{ $r->detalle->observaciones ?? '-' }}</td>
                </tr>
            @empty
                <tr>
                    <td colspan="6" class="text-center">No se encontraron reservas</td>
                </tr>
            @endforelse
        </tbody>
    </table>

    <div class="mt-4">
        <a href="{{ route('reservash.exportar.excel', request()->all()) }}" class="btn btn-success">
            Exportar a Excel
        </a>
        <a href="{{ route('reservash.exportar.pdf', request()->all()) }}" class="btn btn-danger">
            Exportar a PDF
        </a>
    </div>
</div>
@endsection