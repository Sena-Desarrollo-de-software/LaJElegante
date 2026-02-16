@extends('hotel.layouts.header')

@section('title', 'Habitaciones - Hotel LJE')

@section('content')
<div class="container-fluid my-4">
    <div class="row" style="min-height: 80vh;">
        {{-- LeftColum Component: Big Room Frame --}}
        <div class="col-md-6 position-relative d-flex flex-column align-items-center justify-content-between text-center p-4 text-white overflow-hidden habitacion-card"
            style="background: url('{{ asset('build/img/habitacionespecialHotel.png') }}') no-repeat center center/cover; min-height: 80vh;">
            <div class="mb-auto">
                <h4 class="fw-bold">Descubre nuestras habitaciones</h4>
                <p>Confort y elegancia en cada detalle</p> 
            </div>
            <div class="mt-auto pb-3 z-2">
                <a href="#" class="btn btn-reserva btn-lg px-5">Hacer Reserva</a>
            </div>

            <div class="overlay d-flex flex-column justify-content-center align-items-center text-center">
                <h3 class="fw-bold">Habitación Especial</h3>
                <p class="lead">Confort exclusivo y lujo</p>
                <div class="circle-card-2 mt-2">$210.000  noche</div>
            </div>
        </div>

        {{-- RightColumn: grid Rooms --}}
        <div class="col-md-6 ps-3">
            <div class="row g-3 h-100">

                {{-- RoomCard Component --}}
                <div class="col-md-6">
                    <div class="room-card position-relative overflow-hidden h-100">
                        <img src="{{ asset('build/img/habitacionbasicaHotel.png') }}" class="img-fluid w-100 h-100 object-fit-cover" alt="Habitación 1">
                        <div class="room-overlay d-flex flex-column justify-content-center align-items-center text-white">
                            <h5 class="fw-bold">Básica</h5>
                            <span class="badge bg-button-hab fs-6">$70.000</span>
                        </div>
                    </div>
                </div>
                {{-- RoomCard Component --}}
                <div class="col-md-6">
                    <div class="room-card position-relative overflow-hidden h-100">
                        <img src="{{ asset('build/img/habitacionfamiliarHotel.png') }}" class="img-fluid w-100 h-100 object-fit-cover" alt="Habitación 2">
                        <div class="room-overlay d-flex flex-column justify-content-center align-items-center text-white">
                            <h5 class="fw-bold">Familiar</h5>
                            <span class="badge bg-button-hab fs-6">$170.000</span>
                        </div>
                    </div>
                </div>
                {{-- RoomCard Component --}}
                <div class="col-md-6">
                    <div class="room-card position-relative overflow-hidden h-100">
                        <img src="{{ asset('build/img/habitacionparejaHotel.png') }}" class="img-fluid w-100 h-100 object-fit-cover" alt="Habitación 3">
                        <div class="room-overlay d-flex flex-column justify-content-center align-items-center text-white">
                            <h5 class="fw-bold">Pareja</h5>
                            <span class="badge bg-button-hab fs-6">$120.000</span>
                        </div>
                    </div>
                </div>
                {{-- CircleCard Component: Deals --}}
                <div class="col-md-6 d-flex justify-content-center align-items-center">
                    <div class="circle-card-lg">
                        <span class="fw-bold">20% por primera reserva</span>
                    </div>
                </div>

            </div>
        </div>
    </div>
</div>
@endsection