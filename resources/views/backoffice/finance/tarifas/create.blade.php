@extends('backoffice.layouts.tarifas')

@section('content')
    {{-- TopTextForm Component --}}
    <h1 class="mb-4">Nueva Tarifa</h1>
    {{-- CreateForm Component --}}
    <form action="{{ route('tarifas.gestion.store') }}" method="POST">
        @csrf
        {{-- CRUDFormItem Component --}}
        <div class="mb-3">
            {{-- CRUDFormItemInput Component --}}
            <label>Tarifa fija</label>
            <input type="number" step="0.01" name="tarifa_fija" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>Precio final</label>
            <input type="number" step="0.01" name="precio_final" class="form-control" required>
        </div>
        <div class="mb-3">
            {{-- CRUDFormItemSelect Component --}}
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