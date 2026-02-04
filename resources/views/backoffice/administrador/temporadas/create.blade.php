@extends('administrador.layouts.temporadas')

@section('content')
<h2>Nueva Temporada</h2>

<form action="{{ route('temporadas.gestion.store') }}" method="POST">
    @csrf

    <div class="mb-3">
        <label for="nombre" class="form-label">Nombre de la temporada</label>
        <select name="nombre" id="nombre" class="form-control" required>
            <option value="alta">Alta</option>
            <option value="media">Media</option>
            <option value="baja">Baja</option>
        </select>
    </div>

    <div class="mb-3">
        <label for="fecha_inicio" class="form-label">Fecha inicio</label>
        <input type="date" name="fecha_inicio" class="form-control" required>
    </div>

    <div class="mb-3">
        <label for="fecha_fin" class="form-label">Fecha fin</label>
        <input type="date" name="fecha_fin" class="form-control" required>
    </div>

    <div class="mb-3">
        <label for="modificador_precio" class="form-label">Modificador de precio (%)</label>
        <input type="number" step="0.01" name="modificador_precio" class="form-control" required>
    </div>

    <button type="submit" class="btn btn-success">Guardar</button>
    <a href="{{ route('temporadas.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
</form>
@endsection