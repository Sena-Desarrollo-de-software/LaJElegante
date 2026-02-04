@extends('administrador.layouts.users')

@section('title', 'Crear Usuario')

@section('content')
<div class="container">
    <h1 class="mb-4">Crear Usuario</h1>

    <form action="{{ route('users.gestion.store') }}" method="POST">
        @csrf

        <div class="mb-3">
            <label for="name" class="form-label">Nombre</label>
            <input type="text" name="name" id="name" class="form-control" required value="{{ old('name') }}">
            @error('name')
                <div class="text-danger small">{{ $message }}</div>
            @enderror
        </div>

        <div class="mb-3">
            <label for="email" class="form-label">Correo electrónico</label>
            <input type="email" name="email" id="email" class="form-control" required value="{{ old('email') }}">
            @error('email')
                <div class="text-danger small">{{ $message }}</div>
            @enderror
        </div>

        <div class="mb-3">
            <label for="password" class="form-label">Contraseña</label>
            <input type="password" name="password" id="password" class="form-control" required>
            @error('password')
                <div class="text-danger small">{{ $message }}</div>
            @enderror
        </div>

        <div class="mb-3">
            <label for="password_confirmation" class="form-label">Confirmar Contraseña</label>
            <input type="password" name="password_confirmation" id="password_confirmation" class="form-control" required>
        </div>

        <div class="mb-3">
            <label for="role" class="form-label">Rol</label>
            <select name="role" id="role" class="form-select" required>
                <option value="">Seleccione un rol</option>
                <option value="recepcionista" {{ old('role') == 'recepcionista' ? 'selected' : '' }}>Recepcionista</option>
                <option value="asistente_administrativo" {{ old('role') == 'asistente_administrativo' ? 'selected' : '' }}>Asistente administrativo</option>
                <option value="gerente_alimentos" {{ old('role') == 'gerente_alimentos' ? 'selected' : '' }}>Gerente de alimentos</option>
                <option value="gerente_habitaciones" {{ old('role') == 'gerente_habitaciones' ? 'selected' : '' }}>Gerente de habitaciones</option>
                <option value="gerente_general" {{ old('role') == 'gerente_general' ? 'selected' : '' }}>Gerente general</option>
                <option value="administrador" {{ old('role') == 'administrador' ? 'selected' : '' }}>Administrador</option>
            </select>
            @error('role')
                <div class="text-danger small">{{ $message }}</div>
            @enderror
        </div>

        <button type="submit" class="btn btn-success">Guardar</button>
        <a href="{{ route('users.gestion.index') }}" class="btn btn-secondary">Cancelar</a>
    </form>
</div>
@endsection