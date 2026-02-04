@extends('administrador.layouts.clientes')

@section('content')
<div class="container">
    <h1>Editar Cliente</h1>

    <form action="{{ route('clientes.gestion.update', $cliente->id_cliente) }}" method="POST">
        @csrf
        @method('PUT')

        <div class="mb-3">
            <label for="nombre" class="form-label">Nombre</label>
            <input type="text" name="nombre" class="form-control" 
                   value="{{ old('nombre', $cliente->nombre) }}" required>
        </div>

        <div class="mb-3">
            <label for="apellido" class="form-label">Apellido</label>
            <input type="text" name="apellido" class="form-control" 
                   value="{{ old('apellido', $cliente->apellido) }}" required>
        </div>

        <div class="mb-3">
            <label for="email_info" class="form-label">Email</label>
            <input type="email" name="email_info" class="form-control" 
                   value="{{ old('email_info', $cliente->email_info) }}" required>
        </div>

        <div class="mb-3">
            <label for="id_tipo_cliente" class="form-label">Tipo de Cliente</label>
            <select name="id_tipo_cliente" id="id_tipo_cliente" class="form-select" required>
                <option value="">Seleccione un tipo</option>
                @foreach($tipos as $tipo)
                    <option value="{{ $tipo->id_tipo_cliente }}"
                        {{ old('id_tipo_cliente', $cliente->id_tipo_cliente) == $tipo->id_tipo_cliente ? 'selected' : '' }}>
                        {{ $tipo->nombre_tipo }}
                    </option>
                @endforeach
            </select>
        </div>

        <div class="mb-3">
            <label for="prefijo_telefono" class="form-label">Prefijo</label>
            <input type="text" name="prefijo_telefono" class="form-control" 
                   value="{{ old('prefijo_telefono', $cliente->prefijo_telefono) }}">
        </div>

        <div class="mb-3">
            <label for="numero_telefono" class="form-label">Teléfono</label>
            <input type="text" name="numero_telefono" class="form-control" 
                   value="{{ old('numero_telefono', $cliente->numero_telefono) }}">
        </div>

        <div class="mb-3">
            <label for="contrasena" class="form-label">Nueva Contraseña (opcional)</label>
            <input type="password" name="contrasena" class="form-control" placeholder="Deja vacío si no quieres cambiarla">
        </div>

        <div class="mb-3">
            <label for="contrasena_confirmation" class="form-label">Confirmar Contraseña</label>
            <input type="password" name="contrasena_confirmation" class="form-control" placeholder="Confirma la nueva contraseña">
        </div>

        <div class="mb-3">
            <label for="estado" class="form-label">Estado</label>
            <select name="estado" class="form-control" required>
                <option value="activo" {{ old('estado', $cliente->estado) == 'activo' ? 'selected' : '' }}>Activo</option>
                <option value="inactivo" {{ old('estado', $cliente->estado) == 'inactivo' ? 'selected' : '' }}>Inactivo</option>
            </select>
        </div>

        <button type="submit" class="btn btn-primary">Actualizar</button>
        <a href="{{ route('clientes.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection