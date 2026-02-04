@extends('administrador.layouts.app')

@section('title', 'Dashboard - Recepcionista')

@section('content')
<div class="container">
    <h1 class="mb-4">Panel de Recepcionista</h1>

    <div class="row">
        <div class="col-md-6">
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
