@extends('administrador.layouts.reservash')

@section('content')
<h2 class="mb-4">Papelera de Reservas</h2>

<table class="table table-bordered">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Habitación</th>
            <th>Fechas</th>
            <th>Total</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        @forelse($reservas as $reserva)
            <tr>
                <td>{{ $reserva->id_reserva_habitacion }}</td>
                <td>{{ $reserva->cliente->nombre ?? 'N/A' }}</td>
                <td>{{ $reserva->detalle->habitacion->numero_habitacion ?? 'N/A' }}</td>
                <td>{{ $reserva->detalle->fecha_inicio }} → {{ $reserva->detalle->fecha_fin }}</td>
                <td>${{ number_format($reserva->detalle->precio_reserva, 2) }}</td>
                <td>
                    <form action="{{ route('reservash.restaurar', $reserva->id_reserva_habitacion) }}" method="POST" class="d-inline">
                        @csrf
                        @method('PATCH')
                        <button class="btn btn-success btn-sm">Restaurar</button>
                    </form>
                </td>
            </tr>
        @empty
            <tr><td colspan="6" class="text-center">No hay reservas eliminadas.</td></tr>
        @endforelse
    </tbody>
</table>

<a href="{{ route('reservash.gestion.index') }}" class="btn btn-secondary">← Volver</a>
@endsection