@extends('layouts.app')

@section('content')
<div class="container">
    <h1>Detalle de Mesa</h1>

    <ul>
        <li><strong>ID:</strong> {{ $mesa->id_mesa }}</li>
        <li><strong>Número de mesa:</strong> {{ $mesa->numero_mesa }}</li>
        <li><strong>Capacidad:</strong> {{ $mesa->capacidad }}</li>
        <li><strong>Ubicación:</strong> {{ $mesa->ubicacion ?? 'No definida' }}</li>
        <li><strong>Activo:</strong> {{ $mesa->activo ? 'Sí' : 'No' }}</li>
    </ul>

    <a href="{{ route('mesas.index') }}" class="btn btn-secondary">Volver al listado</a>
    <a href="{{ route('mesas.edit', $mesa->id_mesa) }}" class="btn btn-warning">Editar Mesa</a>

    {{-- Botón ocultar/mostrar --}}
    @if($mesa->activo)
        <form action="{{ route('mesas.ocultar', $mesa->id_mesa) }}" method="POST" class="d-inline">
            @csrf
            @method('PATCH')
            <button type="submit" class="btn btn-danger">Ocultar</button>
        </form>
    @else
        <form action="{{ route('mesas.mostrar', $mesa->id_mesa) }}" method="POST" class="d-inline">
            @csrf
            @method('PATCH')
            <button type="submit" class="btn btn-success">Restaurar</button>
        </form>
    @endif
</div>
@endsection
