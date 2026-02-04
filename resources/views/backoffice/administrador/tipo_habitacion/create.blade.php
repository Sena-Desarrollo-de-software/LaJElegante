@extends('administrador.layouts.tipo_habitacion')

@section('content')
<h2>Nuevo Tipo de Habitación</h2>

<form action="{{ route('tipo_habitacion.gestion.store') }}" method="POST" class="card p-4 shadow-sm">
    @csrf

    <div class="mb-3">
        <label class="form-label">Nombre</label>
        <select name="nombre_tipo" class="form-select" required>
            <option value="">Seleccione...</option>
            <option value="familiar">Familiar</option>
            <option value="pareja">Pareja</option>
            <option value="basica">Básica</option>
            <option value="especial">Especial</option>
        </select>
    </div>

    <div class="mb-3">
        <label class="form-label">Descripción</label>
        <textarea name="descripcion" class="form-control" rows="3"></textarea>
    </div>

    <div class="mb-3">
        <label class="form-label">Capacidad Máxima</label>
        <input type="number" name="capacidad_maxima" class="form-control" required>
    </div>

    <button type="submit" class="btn btn-success">Guardar</button>
    <a href="{{ route('tipo_habitacion.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
</form>
@endsection