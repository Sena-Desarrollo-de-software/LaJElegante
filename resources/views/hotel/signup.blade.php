@extends('hotel.layouts.header')

@section('title', 'Registro - Hotel LJE')

@section('content')
<div class="container d-flex justify-content-center align-items-center" style="min-height: 80vh;">
    {{-- CardSignUp Component --}}
    <div class="card shadow-lg p-4" style="max-width: 600px; width: 100%;">
        <h3 class="text-center mb-4 fw-bold"> Crear Cuenta</h3>

        {{-- ErrorMessage Component --}}
        @if ($errors->any())
            <div class="alert alert-danger">
                <ul class="mb-0">
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif
        {{-- SignUpForm Component --}}
        <form method="POST" action="{{ route('hotel.signup.process') }}">
            @csrf

            <input type="hidden" name="id_tipo_cliente" value="1"> 

            <div class="row">
                <div class="col-md-6 mb-3">
                    <label for="nombre" class="form-label">Nombre</label>
                    <input type="text" name="nombre" id="nombre" class="form-control" required>
                </div>

                <div class="col-md-6 mb-3">
                    <label for="apellido" class="form-label">Apellido</label>
                    <input type="text" name="apellido" id="apellido" class="form-control" required>
                </div>
            </div>

            <div class="mb-3">
                <label for="email_info" class="form-label">Correo electrónico</label>
                <input type="email" name="email_info" id="email_info" class="form-control" required>
            </div>

            <div class="mb-3">
                <label for="saludo" class="form-label">Saludo</label>
                <select name="saludo" id="saludo" class="form-select" required>
                    <option value="MR">Sr.</option>
                    <option value="MS">Sra.</option>
                    <option value="MX">Mx.</option>
                </select>
            </div>

            <div class="row">
                <div class="col-md-4 mb-3">
                    <label for="prefijo_telefono" class="form-label">Prefijo</label>
                    <input type="text" name="prefijo_telefono" id="prefijo_telefono" 
                           class="form-control" value="+57" required>
                </div>
                <div class="col-md-8 mb-3">
                    <label for="numero_telefono" class="form-label">Teléfono</label>
                    <input type="text" name="numero_telefono" id="numero_telefono" class="form-control" required>
                </div>
            </div>

            <div class="mb-3">
                <label for="password" class="form-label">Contraseña</label>
                <input type="password" name="password" id="password" 
                    class="form-control" placeholder="Mínimo 8 caracteres" required>
            </div>

            <div class="mb-3">
                <label for="password_confirmation" class="form-label">Confirmar Contraseña</label>
                <input type="password" name="password_confirmation" id="password_confirmation" 
                    class="form-control" placeholder="Repite la contraseña" required>
            </div>

            <button type="submit" class="btn btn-reserva w-100">Registrar</button>
        </form>

        <hr class="my-4">
        {{-- AditionalMessageForm Component --}}
        <p class="text-center mb-0">
            ¿Ya tienes cuenta?
            <a href="{{ route('hotel.login.index') }}" class="fw-bold text-primary">Inicia sesión aquí</a>
        </p>
    </div>
</div>
@endsection