@extends('administrador.layouts.app')

@section('title', 'Dashboard - Sistema de Reservas')

@section('content')
<div class="container">

    <h1 class="mb-4">Panel de Administración</h1>

    {{-- Tarjetas resumen --}}
    <div class="row text-center mb-4">
        <div class="col-md-3">
            <div class="card text-bg-primary shadow">
                <div class="card-body">
                    <h5 class="card-title">Clientes</h5>
                    <h2>{{ $clientesCount ?? 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-bg-success shadow">
                <div class="card-body">
                    <h5 class="card-title">Usuarios</h5>
                    <h2>{{ $usuariosCount ?? 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-bg-warning shadow">
                <div class="card-body">
                    <h5 class="card-title">Habitaciones</h5>
                    <h2>{{ $habitacionesCount ?? 0 }}</h2>
                </div>
            </div>
        </div>

        <div class="col-md-3">
            <div class="card text-bg-danger shadow">
                <div class="card-body">
                    <h5 class="card-title">Reservas Activas</h5>
                    <h2>{{ $reservasActivas ?? 0 }}</h2>
                </div>
            </div>
        </div>
    </div>

    {{-- Gráficas --}}
    <div class="row">
        <div class="col-md-6 mb-4">
            <div class="card shadow">
                <div class="card-body">
                    <h5 class="card-title">Reservas por Mes</h5>
                    <canvas id="reservasChart" style="height:300px;"></canvas>
                </div>
            </div>
        </div>

        <div class="col-md-6 mb-4">
            <div class="card shadow">
                <div class="card-body">
                    <h5 class="card-title">Ocupación de Habitaciones</h5>
                    <canvas id="ocupacionChart" style="height:300px;"></canvas>
                </div>
            </div>
        </div>
    </div>

    
    
</div>
@endsection

@section('scripts')
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Reservas por Mes
    const ctxReservas = document.getElementById('reservasChart').getContext('2d');
    new Chart(ctxReservas, {
        type: 'bar',
        data: {
            labels: @json($mesesLabels ?? []),
            datasets: [{
                label: 'Reservas',
                data: @json($reservasPorMes ?? []),
                backgroundColor: '#0d6efd'
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true }
            }
        }
    });

    // Ocupación
    const ctxOcupacion = document.getElementById('ocupacionChart').getContext('2d');
    new Chart(ctxOcupacion, {
        type: 'doughnut',
        data: {
            labels: ['Ocupadas', 'Disponibles'],
            datasets: [{
                data: @json($ocupacion ?? [0, 0]),
                backgroundColor: ['#dc3545', '#198754']
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false 
        }
    });
</script>
@endsection
