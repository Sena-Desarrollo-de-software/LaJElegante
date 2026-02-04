@extends('administrador.layouts.habitaciones')

@section('content')
<div class="container mt-4">
    <h1 class="mb-4">Reporte de Habitaciones</h1>

    {{-- Formulario de filtros --}}
    <form method="GET" action="{{ route('habitaciones.reportes') }}" class="row g-3 mb-4">
        <div class="col-md-3">
            <label class="form-label">Estado</label>
            <select name="estado_habitacion" class="form-select">
                <option value="">Todas</option> 
                <option value="en servicio" {{ request('estado_habitacion') == 'disponible' ? 'selected' : '' }}>En servicio</option>
                <option value="ocupada" {{ request('estado_habitacion') == 'ocupada' ? 'selected' : '' }}>Ocupada</option>
                <option value="mantenimiento" {{ request('estado_habitacion') == 'mantenimiento' ? 'selected' : '' }}>Mantenimiento</option>
            </select>
        </div>

        <div class="col-md-3">
            <label class="form-label">Tipo de Habitación</label>
            <select name="tipo" class="form-select">
                <option value="">Todas</option>
                @foreach($tipos as $tipo)
                    <option value="{{ $tipo->id_tipo_habitacion }}" {{ request('tipo') == $tipo->id_tipo_habitacion ? 'selected' : '' }}>
                        {{ $tipo->nombre_tipo }}
                    </option>
                @endforeach
            </select>
        </div>

        <div class="col-md-3">
            <label class="form-label">Rango de fechas</label>
            <input type="date" name="desde" class="form-control" value="{{ request('desde') }}">
            <input type="date" name="hasta" class="form-control mt-1" value="{{ request('hasta') }}">
        </div>

        <div class="col-md-3 d-flex align-items-end">
            <button type="submit" class="btn btn-primary">Filtrar</button>
        </div>
    </form>

    {{-- Botones de exportación --}}
    <div class="mb-3">
        <a href="{{ route('habitaciones.exportar.excel', request()->all()) }}" class="btn btn-success">
            Exportar Excel
        </a>

        <a href="{{ route('habitaciones.exportar.pdf', request()->all()) }}" class="btn btn-danger">
            Exportar PDF
        </a>
    </div>

    {{-- Tabla de resultados --}}
    @if($habitaciones->count())
    <table class="table table-bordered">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Número</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Creado</th>
            </tr>
        </thead>
        <tbody>
            @foreach($habitaciones as $habitacion)
            <tr>
                <td>{{ $habitacion->id_habitacion }}</td>
                <td>{{ $habitacion->numero_habitacion }}</td>
                <td>{{ $habitacion->tipoHabitacion->nombre_tipo ?? 'Sin tipo' }}</td>
                <td>{{ ucfirst($habitacion->estado_habitacion) }}</td>
                <td>{{ $habitacion->created_at->format('d/m/Y H:i') }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
    @else
    <div class="alert alert-info">No hay habitaciones que coincidan con los filtros.</div>
    @endif
</div>
@endsection