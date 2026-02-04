@extends('administrador.layouts.temporadas')

@section('content')
<h2>Papelera de Temporadas</h2>

@if(session('success'))
<div class="alert alert-success">{{ session('success') }}</div>
@endif

<table class="table table-bordered">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Inicio</th>
            <th>Fin</th>
            <th>Modificador</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        @forelse($temporadas as $temporada)
        <tr>
            <td>{{ $temporada->id_temporada }}</td>
            <td>{{ ucfirst($temporada->nombre) }}</td>
            <td>{{ $temporada->fecha_inicio }}</td>
            <td>{{ $temporada->fecha_fin }}</td>
            <td>{{ $temporada->modificador_precio }}%</td>
            <td>
                <form action="{{ route('temporadas.restaurar', $temporada->id_temporada) }}" method="POST">
                    @csrf
                    @method('PATCH')
                    <button class="btn btn-success btn-sm">Restaurar</button>
                </form>
            </td>
        </tr>
        @empty
        <tr><td colspan="6" class="text-center">No hay temporadas eliminadas</td></tr>
        @endforelse
    </tbody>
</table>

<a href="{{ route('temporadas.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
@endsection