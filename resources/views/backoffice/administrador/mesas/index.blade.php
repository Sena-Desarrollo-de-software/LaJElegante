@extends('administrador.layouts.app')

@section('content')
<div class="container">
    <h1>Listado de Mesas</h1>

    {{-- Botón para crear nueva mesa --}}
    <a href="{{ route('mesas.gestion.create') }}" class="btn btn-success mb-3">Nueva Mesa</a>

    <a href="{{ route('mesas.exportExcel') }}" class="btn btn-primary mb-3">Exportar Excel</a>
    <a href="{{ route('mesas.exportPDF') }}" class="btn btn-danger mb-3">Exportar PDF</a>

    {{-- Mensajes de éxito --}}
    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    {{-- Filtro para mostrar mesas ocultas --}}
    <form method="GET" class="mb-3">
        <label>
            <input type="checkbox" name="mostrar_ocultos" value="1" {{ request('mostrar_ocultos') ? 'checked' : '' }}>
            Mostrar mesas ocultas
        </label>
        <button type="submit" class="btn btn-primary btn-sm">Filtrar</button>
    </form>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>Número</th>
                <th>Capacidad</th>
                <th>Ubicación</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse($mesas as $mesa)
                <tr>
                    <td>{{ $mesa->id_mesa }}</td>
                    <td>{{ $mesa->numero_mesa }}</td>
                    <td>{{ $mesa->capacidad }}</td>
                    <td>{{ $mesa->ubicacion }}</td>
                    <td>{{ $mesa->activo ? 'Sí' : 'No' }}</td>
                    <td>
                        <a href="{{ route('mesas.gestion.show', $mesa->id_mesa) }}" class="btn btn-info btn-sm">Ver</a>
                        <a href="{{ route('mesas.gestion.edit', $mesa->id_mesa) }}" class="btn btn-warning btn-sm">Editar</a>

                        {{-- Eliminar (papelera) --}}
                        @if($mesa->activo)
                            <form action="{{ route('mesas.ocultar', $mesa->id_mesa) }}" method="POST" class="d-inline">
                                @csrf
                                @method('PATCH')
                                <button type="submit" class="btn btn-danger btn-sm">Eliminar</button>
                            </form>
                        @else
                            {{-- Restaurar --}}
                            <form action="{{ route('mesas.mostrar', $mesa->id_mesa) }}" method="POST" class="d-inline">
                                @csrf
                                @method('PATCH')
                                <button type="submit" class="btn btn-success btn-sm">Restaurar</button>
                            </form>
                        @endif
                    </td>
                </tr>
            @empty
                <tr><td colspan="6">No hay mesas registradas.</td></tr>
            @endforelse
        </tbody>
    </table>
</div>
@endsection
