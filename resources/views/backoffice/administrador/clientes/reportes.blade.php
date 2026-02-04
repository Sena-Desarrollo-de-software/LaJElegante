@extends('administrador.layouts.clientes')

@section('content')
<div class="container mt-4">
    <h1 class="mb-4">Reporte de Clientes</h1>

    <form method="GET" action="{{ route('clientes.reportes') }}" class="row g-3 mb-4">
        <div class="col-md-3">
            <label class="form-label">Estado</label>
            <select name="estado" class="form-select">
                <option value="">Todos</option>
                <option value="activo" {{ request('estado') == 'activo' ? 'selected' : '' }}>Activo</option>
                <option value="inactivo" {{ request('estado') == 'inactivo' ? 'selected' : '' }}>Inactivo</option>
            </select>
        </div>

        <div class="col-md-3">
            <label class="form-label">Tipo Cliente</label>
            <select name="tipo" class="form-select">
                <option value="">Todos</option>
                @foreach($tipos as $tipo)
                    <option value="{{ $tipo->id_tipo_cliente }}" {{ request('tipo') == $tipo->id_tipo_cliente ? 'selected' : '' }}>
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

    <div class="mb-3">
        <a href="{{ route('clientes.exportar.excel', request()->all()) }}" class="btn btn-success">
            Exportar Excel
        </a>

        <a href="{{ route('clientes.exportar.pdf', request()->all()) }}" class="btn btn-danger">
            Exportar PDF
        </a>
    </div>

    @if($clientes->count())
    <table class="table table-bordered">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Nombre completo</th>
                <th>Email</th>
                <th>Tipo Cliente</th>
                <th>Telefono</th>
                <th>Estado</th>
            </tr>
        </thead>
        <tbody>
            @foreach($clientes as $cliente)
            <tr>
                <td>{{ $cliente->id_cliente }}</td>
                <td>{{ $cliente->nombre }} {{ $cliente->apellido }}</td>
                <td>{{ $cliente->email_info }}</td>
                <td>{{ $cliente->tipoCliente->nombre ?? 'Sin tipo' }}</td>
                <td>{{ $cliente->telefono }}</td>
                <td>{{ ucfirst($cliente->estado) }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
    @else
    <div class="alert alert-info">No hay clientes que coincidan con los filtros.</div>
    @endif
</div>
@endsection