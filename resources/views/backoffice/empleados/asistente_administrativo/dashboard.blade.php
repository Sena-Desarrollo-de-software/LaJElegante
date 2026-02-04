@extends('administrador.layouts.app')

@section('title', 'Dashboard - Asistente Administrativo')

@section('content')
<div class="container">
    <h1 class="mb-4">Panel de Asistente Administrativo</h1>

    <div class="row">
        <div class="col-md-4">
            <div class="card text-bg-success mb-3 shadow">
                <div class="card-body">
                    <h5 class="card-title">Usuarios</h5>
                    <p class="card-text">Administrar los usuarios internos del sistema.</p>
                    <a href="{{ route('users.gestion.index') }}" class="btn btn-light btn-sm">Ir</a>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card text-bg-primary mb-3 shadow">
                <div class="card-body">
                    <h5 class="card-title">Clientes</h5>
                    <p class="card-text">Gestiona todos los clientes registrados.</p>
                    <a href="{{ route('clientes.gestion.index') }}" class="btn btn-light btn-sm">Ir</a>
                </div>
            </div>
        </div>

        <div class="col-md-4">
            <div class="card text-bg-warning mb-3 shadow">
                <div class="card-body">
                    <h5 class="card-title">Reservas Restaurante</h5>
                    <p class="card-text">Controla y organiza las reservas.</p>
                    <a href="{{ route('reservasr.gestion.index') }}" class="btn btn-light btn-sm">Ir</a>
                </div>
            </div>
        </div>
                <div class="col-md-4">
            <div class="card text-bg-warning mb-3 shadow">
                <div class="card-body">
                    <h5 class="card-title">Reservas Habitaciones</h5>
                    <p class="card-text">Controla y organiza las reservas.</p>
                    <a href="{{ route('reservash.gestion.index') }}" class="btn btn-light btn-sm">Ir</a>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
