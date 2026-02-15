<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gestión Clientes</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ asset('build/assets/js/clientes.js') }}"></script>
</head>
<body>
    
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="{{ route('administrador.dashboard') }}">Clientes</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTipoCliente">
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="navbarTipoCliente">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                    <li class="nav-item">
                        <a class="nav-link" href="{{ route('clientes.gestion.index') }}">Listado</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ route('clientes.gestion.create') }}">+ Nuevo</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ route('clientes.papelera') }}">Papelera</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{{ route('clientes.reportes') }}">Reportes</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        @yield('content')
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    @yield('charts')
</body>
</html>