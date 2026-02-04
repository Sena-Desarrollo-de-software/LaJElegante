@extends('layouts.app')

@section('content')
<div class="container">
    <h1>Editar Mesa</h1>

    <form action="{{ route('mesas.update', $mesa->id_mesa) }}" method="POST">
        @csrf
        @method('PUT')

        <div class="mb-3">
            <label for="numero_mesa" class="form-label">Número de Mesa</label>
            <input type="number" name="numero_mesa" class="form-control" value="{{ old('numero_mesa', $mesa->numero_mesa) }}" required>
        </div>

        <div class="mb-3">
            <label for="capacidad" class="form-label">Capacidad</label>
            <input type="number" name="capacidad" class="form-control" value="{{ old('capacidad', $mesa->capacidad) }}" required>
        </div>

        <div class="mb-3">
            <label for="ubicacion" class="form-label">Ubicación</label>
            <input type="text" name="ubicacion" class="form-control" value="{{ old('ubicacion', $mesa->ubicacion) }}">
        </div>

        {{-- Estado activo (opcional mostrar/editar) --}}
        <div class="mb-3 form-check">
            <input type="checkbox" name="activo" class="form-check-input" id="activo" value="1" {{ $mesa->activo ? 'checked' : '' }}>
            <label class="form-check-label" for="activo">Activo</label>
        </div>

        <button type="submit" class="btn btn-primary">Actualizar Mesa</button>
        <a href="{{ route('mesas.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection
