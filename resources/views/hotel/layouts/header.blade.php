<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>@yield('title', 'Hotel La J Elegante')</title>
    {{-- Inyectar bootstrap local --}}
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="{{ asset('build/assets/css/index.css') }}">
    <link rel="icon" href="{{ asset('build/img/icons/logoHotel.png') }}">
</head>
<body>
{{-- HotelNavBar Component--}}
<nav class="navbar navbar-expand-lg background-nav-hotel navbar-dark py-3">
    <div class="container-fluid">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarHotel">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarHotel">
            <ul class="navbar-nav w-100 d-flex justify-content-between text-center">
                {{-- NavBarItem Component --}}
                <li class="nav-item flex-fill">
                    <a class="nav-link d-flex flex-column align-items-center" href="{{ route('hotel.lobby.index') }}">
                        <img src="{{ asset('build/img/icons/lobby.png') }}" alt="Lobby" style="width:50px; height:50px;">
                        <span class="mt-1">Lobby</span>
                    </a>
                </li>

                {{-- NavBarItem Component --}}
                <li class="nav-item flex-fill">
                    <a class="nav-link d-flex flex-column align-items-center" href="{{ route('hotel.restaurante.index') }}">
                        <img src="{{ asset('build/img/icons/restaurante.png') }}" alt="Restaurante" style="width:50px; height:50px;">
                        <span class="mt-1">Restaurante</span>
                    </a>
                </li>

                {{-- NavBarItem Component --}}
                <li class="nav-item flex-fill">
                    <a class="nav-link d-flex flex-column align-items-center" href="{{ route('hotel.habitaciones.index') }}">
                        <img src="{{ asset('build/img/icons/habitaciones.png') }}" alt="Habitaciones" style="width:50px; height:50px;">
                        <span class="mt-1">Habitaciones</span>
                    </a>
                </li>

                {{-- NavBarItem Component --}}
                <li class="nav-item flex-fill">
                    <a class="nav-link d-flex flex-column align-items-center" href="{{ route('hotel.terminos.index') }}">
                        <img src="{{ asset('build/img/icons/terminos.png') }}" alt="Términos" style="width:50px; height:50px;">
                        <span class="mt-1">T&C</span>
                    </a>
                </li>

                {{-- NavBarItem Component --}}
                <li class="nav-item flex-fill">
                    <a class="nav-link d-flex flex-column align-items-center" href="{{ route('hotel.login.index') }}">
                        <img src="{{ asset('build/img/icons/login.png') }}" alt="Login" style="width:50px; height:50px;">
                        <span class="mt-1">Login</span>
                    </a>
                </li>
            </ul>
        </div>
    </div>
</nav>
    {{-- DinamicContent Component --}}
    <main class="container mt-4">
        @yield('content')
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>