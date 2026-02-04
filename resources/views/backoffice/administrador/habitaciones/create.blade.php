@extends('administrador.layouts.habitaciones')

@section('content')
    <h1 class="mb-4">Nueva Habitación</h1>

    <form action="{{ route('habitaciones.gestion.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label class="form-label">Número de Habitación</label>
            <input type="text" name="numero_habitacion" class="form-control" maxlength="3" required>
        </div>

        <div class="mb-3">
            <label class="form-label">Tipo de Habitación</label>
            <select name="id_tipo_habitacion" class="form-select" required>
                <option value="">Seleccione un tipo</option>
                @foreach(\App\Models\TipoHabitacion::all() as $tipo)
                    <option value="{{ $tipo->id_tipo_habitacion }}">{{ $tipo->nombre_tipo }}</option>
                @endforeach
            </select>
        </div>

        <div class="mb-3">
            <label class="form-label">Estado</label>
            <select name="estado_habitacion" class="form-select" required>
                <option value="en servicio">En servicio</option>
                <option value="mantenimiento">Mantenimiento</option>
                <option value="inactiva">Inactiva</option>
            </select>
        </div>

        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{{ route('habitaciones.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
@endsection
