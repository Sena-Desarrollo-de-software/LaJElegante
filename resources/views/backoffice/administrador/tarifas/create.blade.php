@extends('administrador.layouts.tarifas')

@section('content')
    <h1 class="mb-4">Nueva Tarifa</h1>

    <form action="{{ route('tarifas.gestion.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label>Tarifa fija</label>
            <input type="number" step="0.01" name="tarifa_fija" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Precio final</label>
            <input type="number" step="0.01" name="precio_final" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Estado</label>
            <select name="estado" class="form-select">
                <option value="vigente">Vigente</option>
                <option value="inactiva">Inactiva</option>
            </select>
        </div>
        <div class="mb-3">
            <label>Temporada</label>
            <select name="id_temporada" class="form-select">
                @foreach($temporadas as $temporada)
                    <option value="{{ $temporada->id_temporada }}">{{ ucfirst($temporada->nombre) }}</option>
                @endforeach
            </select>
        </div>
        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{{ route('tarifas.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
@endsection