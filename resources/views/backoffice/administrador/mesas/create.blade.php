@extends('administrador.layouts.mesas')

@section('content')
<div class="container">
    <h1>Crear Nueva Mesa</h1>

    <form action="{{ route('mesas.store') }}" method="POST">
        @csrf

        <div class="mb-3">
            <label for="numero_mesa" class="form-label">Número de Mesa</label>
            <input type="number" name="numero_mesa" class="form-control" value="{{ old('numero_mesa') }}" required>
        </div>

        <div class="mb-3">
            <label for="capacidad" class="form-label">Capacidad</label>
            <input type="number" name="capacidad" class="form-control" value="{{ old('capacidad') }}" required>
        </div>

        <div class="mb-3">
            <label for="ubicacion" class="form-label">Ubicación</label>
            <input type="text" name="ubicacion" class="form-control" value="{{ old('ubicacion') }}">
        </div>

        {{-- Checkbox activo por defecto --}}
        <div class="mb-3 form-check">
            <input type="checkbox" name="activo" class="form-check-input" id="activo" value="1" checked>
            <label class="form-check-label" for="activo">Activo</label>
        </div>

        <button type="submit" class="btn btn-primary">Guardar Mesa</button>
        <a href="{{ route('mesas.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection
