@extends('hotel.layouts.header')

@section('title', 'Lobby - Hotel LJE')

@section('content')
<div class="container text-center">
    {{-- Carousel Component --}}
    <div id="carouselLobby" class="carousel slide w-100 mx-auto mb-4" data-bs-ride="carousel">
        <div class="carousel-inner">
            {{-- CarouselItem Component --}}
            <div class="carousel-item active position-relative">
                <img src="{{ asset('build/img/hotel2.png') }}" class="d-block w-100 rounded" alt="Lobby 1">
                <div class="carousel-caption d-flex flex-column justify-content-center h-100">
                    <h2 class="text-white fw-bold">Bienvenido al Hotel La J Elegante</h2>
                    <p class="lead">Tu descanso y confort en un solo lugar</p>
                </div>
            </div>
            {{-- CarouselItem Component --}}
            <div class="carousel-item position-relative">
                <img src="{{ asset('build/img/restauranteHotel2.png') }}" class="d-block w-100 rounded" alt="Lobby 2">
                <div class="carousel-caption d-flex flex-column justify-content-center h-100">
                    <h2 class="text-white fw-bold">Experiencias únicas</h2>
                    <p class="lead">Restaurante gourmet y servicio exclusivo</p>
                </div>
            </div>
            {{-- CarouselItem Component --}}
            <div class="carousel-item position-relative">
                <img src="{{ asset('build/img/fondologinHotel.png') }}" class="d-block w-100 rounded" alt="Lobby 3">
                <div class="carousel-caption d-flex flex-column justify-content-center h-100">
                    <h2 class="text-white fw-bold">Relájate en nuestras habitaciones</h2>
                    <p class="lead">Comodidad y estilo al alcance de tu mano</p>
                </div>
            </div>
        </div>

        <button class="carousel-control-prev" type="button" data-bs-target="#carouselLobby" data-bs-slide="prev">
            <span class="carousel-control-prev-icon"></span>
        </button>
        <button class="carousel-control-next" type="button" data-bs-target="#carouselLobby" data-bs-slide="next">
            <span class="carousel-control-next-icon"></span>
        </button>
    </div>
    {{-- BottomNav Component --}}
    <div class="row justify-content-center mt-3">
        {{-- BottomNavRoute Component --}}
        <div class="col-md-4 mb-4">
            <a href="{{ route('hotel.restaurante.index') }}" class="btn btn-color btn-lg w-100 text-white">Restaurante</a>
        </div>
        {{-- BottomNavRoute Component --}}
        <div class="col-md-4 mb-4">
            <a href="{{ route('hotel.habitaciones.index') }}" class="btn btn-color btn-lg w-100 text-white">Habitaciones</a>
        </div>
        {{-- BottomNavRoute Component --}}
        <div class="col-md-4 mb-4">
            <a href="{{ route('hotel.terminos.index') }}" class="btn btn-color btn-lg w-100 text-white">Términos & Condiciones</a>
        </div>
    </div>
    
</div>
@endsection