@extends('administrador.layouts.tipo_cliente')

@section('content')
<div class="container mt-4">
    <h1 class="mb-4">Crear Tipo de Cliente</h1>

    {{-- Mostrar errores de validación --}}
    @if($errors->any())
        <div class="alert alert-danger">
            <ul>
                @foreach($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form action="{{ route('tipo_cliente.gestion.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label for="nombre_tipo" class="form-label">Nombre del Tipo</label>
            <input type="text" name="nombre_tipo" id="nombre_tipo" 
                   class="form-control" value="{{ old('nombre_tipo') }}" required>
        </div>

        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{{ route('tipo_cliente.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection