@extends('hotel.layouts.header')

@section('title', 'Términos y Condiciones - Hotel LJE')

@section('content')
<div class="container my-5">
    <h2 class="text-center fw-bold mb-4 text-white">📜 Términos y Condiciones</h2>
    
    {{-- Fila 1 --}}
    <div class="row g-3">
        <div class="col-md-4">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Uso Responsable</h5>
                <p>Los huéspedes deben respetar las normas del hotel y a los demás clientes.</p>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Reservas</h5>
                <p>Las reservas deben confirmarse con 48h de anticipación.</p>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Check-in</h5>
                <p>Desde las 3:00 PM hasta las 11:00 AM (check-out).</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Cancelaciones</h5>
                <p>Notificar mínimo con 24h de anticipación para evitar cargos.</p>
            </div>
        </div>
    </div>

    {{-- Fila 2 --}}
    <div class="row g-3 mt-3">
        <div class="col-md-2">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Mascotas</h5>
                <p>Permitidas solo en áreas designadas del hotel.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Pagos</h5>
                <p>Aceptamos tarjetas y efectivo en moneda local.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Responsabilidad</h5>
                <p>El hotel no se hace responsable por objetos de valor no declarados.</p>
            </div>
        </div>
        <div class="col-md-2">
            <div class="card bg-dark text-white h-100 shadow-sm p-3">
                <h5 class="fw-bold">Ruido</h5>
                <p>Se prohíben ruidos fuertes después de las 10:00 PM.</p>
            </div>
        </div>
    </div>
</div>
@endsection