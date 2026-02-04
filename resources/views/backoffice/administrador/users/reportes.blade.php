@extends('administrador.layouts.users')

@section('content')
<div class="container mt-4">
    <h1 class="mb-4">Reporte de Usuarios</h1>

    {{-- Formulario de filtros --}}
    <form method="GET" action="{{ route('users.reportes') }}" class="row g-3 mb-4">
        <div class="col-md-3">
            <label class="form-label">Rol</label>
            <select name="role" class="form-select">
                <option value="">Todos</option>
                @foreach(['recepcionista','asistente_administrativo','gerente_alimentos','gerente_habitaciones','gerente_general','administrador'] as $rol)
                    <option value="{{ $rol }}" {{ request('role') == $rol ? 'selected' : '' }}>
                        {{ ucfirst(str_replace('_',' ', $rol)) }}
                    </option>
                @endforeach
            </select>
        </div>

        <div class="col-md-3">
            <label class="form-label">Fecha de creación</label>
            <input type="date" name="desde" class="form-control" value="{{ request('desde') }}">
            <input type="date" name="hasta" class="form-control mt-1" value="{{ request('hasta') }}">
        </div>

        <div class="col-md-3 d-flex align-items-end">
            <button type="submit" class="btn btn-primary">Filtrar</button>
        </div>
    </form>

    <div class="mb-3">
        <a href="{{ route('users.exportar.excel', request()->all()) }}" class="btn btn-success">
            Exportar Excel
        </a>
        <a href="{{ route('users.exportar.pdf', request()->all()) }}" class="btn btn-danger">
            Exportar PDF
        </a>
    </div>

    {{-- Tabla de resultados --}}
    @if($usuarios->count())
        <table class="table table-bordered">
            <thead class="table-dark">
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Rol</th>
                    <th>Creado en</th>
                </tr>
            </thead>
            <tbody>
                @foreach($usuarios as $usuario)
                <tr>
                    <td>{{ $usuario->id }}</td>
                    <td>{{ $usuario->name }}</td>
                    <td>{{ $usuario->email }}</td>
                    <td>{{ ucfirst(str_replace('_',' ', $usuario->role)) }}</td>
                    <td>{{ $usuario->created_at->format('d/m/Y') }}</td>
                </tr>
                @endforeach
            </tbody>
        </table>
    @else
        <div class="alert alert-info">No hay usuarios que coincidan con los filtros.</div>
    @endif
</div>
@endsection