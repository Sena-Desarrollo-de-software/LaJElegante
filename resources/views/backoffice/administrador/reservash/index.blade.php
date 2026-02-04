@extends('administrador.layouts.reservash')

@section('content')
<h2 class="mb-4">Listado de Reservas</h2>

<table class="table table-bordered">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Cliente</th>
            <th>Habitación</th>
            <th>Fechas</th>
            <th>Noches</th>
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
                <td>{{ $reserva->detalle->noches }}</td>
                <td>${{ number_format($reserva->detalle->precio_reserva, 2) }}</td>
                <td>
                    <form action="{{ route('reservash.gestion.destroy', $reserva->id_reserva_habitacion) }}" method="POST" class="d-inline">
                        @csrf
                        @method('DELETE')
                        <button class="btn btn-danger btn-sm" onclick="return confirm('¿Seguro que deseas eliminar esta reserva?')">Eliminar</button>
                    </form>
                </td>
            </tr>
        @empty
            <tr><td colspan="7" class="text-center">No hay reservas registradas.</td></tr>
        @endforelse
    </tbody>
</table>
@endsection