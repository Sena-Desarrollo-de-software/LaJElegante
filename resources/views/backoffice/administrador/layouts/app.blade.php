<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'Sistema de Reservas')</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            min-height: 100vh;
            display: flex;
        }
        /* Sidebar fijo en pantallas grandes */
        .sidebar {
            width: 250px;
            flex-shrink: 0;
            background-color: #343a40;
        }
        .sidebar .nav-link {
            color: #fff;
        }
        .sidebar .nav-link.active {
            background-color: #495057;
            font-weight: bold;
        }
        .content {
            flex-grow: 1;
            padding: 20px;
            background: #f8f9fa;
            width: 100%;
        }
        /* Ocultar sidebar en responsive */
        @media (max-width: 991px) {
            .sidebar {
                display: none;
            }
        }
    </style>
</head>
<body>

    <div class="sidebar d-none d-lg-flex flex-column p-3">
        <h4 class="text-white">Sistema Hotel</h4>
        <ul class="nav nav-pills flex-column mb-auto">
            <li class="nav-item"><a href="{{ route('clientes.gestion.index') }}" class="nav-link">Clientes</a></li>
            <li><a href="{{ route('users.gestion.index') }}" class="nav-link">Usuarios</a></li>
            <li><a href="{{ route('habitaciones.gestion.index') }}" class="nav-link">Habitaciones</a></li>
            <li><a href="{{ route('reservash.gestion.index') }}" class="nav-link">Reservas Habitacion</a></li>
            <li><a href="{{ route('tipo_cliente.gestion.index') }}" class="nav-link">Tipos de Cliente</a></li>
            <li><a href="{{ route('tipo_habitacion.gestion.index') }}" class="nav-link">Tipos de Habitación</a></li>
            <li><a href="{{ route('tarifas.gestion.index') }}" class="nav-link">Tarifas</a></li>
            <li><a href="{{ route('temporadas.gestion.index') }}" class="nav-link">Temporadas</a></li>
            <li class="nav-item"><a class="nav-link" href="{{ route('mesas.gestion.index') }}">Mesas</a></li>
            <li><a href="{{ route('reservasr.gestion.index') }}" class="nav-link">Reservas Restaurante</a></li>
        </ul>

        <hr>
            <form action="{{ route('hotel.empleados.logout') }}" method="POST">
                @csrf
                <button type="submit" class="btn btn-danger w-100">Salir</button>
            </form>
    </div>

    <div class="content">
        <nav class="navbar navbar-dark bg-dark mb-4 d-lg-none">
            <div class="container-fluid">
                <button class="btn btn-outline-light" type="button" data-bs-toggle="offcanvas" data-bs-target="#mobileSidebar">
                    ☰ Menú
                </button>
                <span class="navbar-brand">Sistema Hotel</span>
            </div>
        </nav>

        @yield('content')
    </div>

    <div class="offcanvas offcanvas-start bg-dark text-white" tabindex="-1" id="mobileSidebar">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title">Menú</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button>
        </div>
        <div class="offcanvas-body">
            <ul class="nav nav-pills flex-column mb-auto">
                <li class="nav-item"><a href="{{ route('clientes.gestion.index') }}" class="nav-link text-white">Clientes</a></li>
                <li><a href="{{ route('users.gestion.index') }}" class="nav-link text-white">Usuarios</a></li>
                <li><a href="{{ route('habitaciones.gestion.index') }}" class="nav-link text-white">Habitaciones</a></li>
                <li><a href="{{ route('reservash.gestion.index') }}" class="nav-link text-white">Reservas Habitaciones</a></li>
                <li><a href="{{ route('tipo_cliente.gestion.index') }}" class="nav-link text-white">Tipos de Cliente</a></li>
                <li><a href="{{ route('tipo_habitacion.gestion.index') }}" class="nav-link text-white">Tipos de Habitación</a></li>
                <li><a href="{{ route('tarifas.gestion.index') }}" class="nav-link text-white">Tarifas</a></li>
                <li><a href="{{ route('temporadas.gestion.index') }}" class="nav-link text-white">Temporadas</a></li>
                <li class="nav-item"><a class="nav-link" href="{{ route('mesas.gestion.index') }}">Mesas</a></li>
                <li class="nav-item"><a class="nav-link" href="{{ route('reservasr.gestion.index') }}">Reservas Restaurante</a></li>
            </ul>

            <hr>
                <form action="{{ route('hotel.empleados.logout') }}" method="POST">
                    @csrf
                    <button type="submit" class="btn btn-danger w-100">Salir</button>
                </form>
        </div>


    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>

<div class="position-fixed bottom-0 end-0 p-3" style="z-index: 11">
    <div id="logoutToast" class="toast align-items-center text-white bg-success border-0" role="alert" aria-live="assertive" aria-atomic="true">
        <div class="d-flex">
            <div class="toast-body">
                Sesión cerrada correctamente.
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Cerrar"></button>
        </div>
    </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function () {
    @if(session('success'))
        var toastEl = document.getElementById('logoutToast');
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
    @endif
});
</script>

</body>
</html>