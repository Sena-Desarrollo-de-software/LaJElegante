@extends('administrador.layouts.tipo_habitacion')

@section('content')
<h2>Papelera de Tipos de Habitación</h2>

@if(session('success'))
    <div class="alert alert-success">{{ session('success') }}</div>
@endif

<table class="table table-bordered table-striped">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Capacidad</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        @forelse($tipos as $tipo)
            <tr>
                <td>{{ $tipo->id_tipo_habitacion }}</td>
                <td>{{ ucfirst($tipo->nombre_tipo) }}</td>
                <td>{{ $tipo->descripcion }}</td>
                <td>{{ $tipo->capacidad_maxima }}</td>
                <td>
                    <form action="{{ route('tipo_habitacion.restaurar', $tipo->id_tipo_habitacion) }}" method="POST" class="d-inline">
                        @csrf
                        @method('PATCH')
                        <button class="btn btn-primary btn-sm">Restaurar</button>
                    </form>
                </td>
            </tr>
        @empty
            <tr>
                <td colspan="5" class="text-center">No hay tipos de habitación en la papelera</td>
            </tr>
        @endforelse
    </tbody>
</table>

<a href="{{ route('tipo_habitacion.gestion.index') }}" class="btn btn-secondary">← Volver</a>
@endsection