@extends('administrador.layouts.reservasr')

@section('content')
<div class="container">
    <h1>Listado de Reservas</h1>

    {{-- Botón para crear nueva reserva --}}
    <a href="{{ route('reservasr.gestion.create') }}" class="btn btn-success mb-3">Nueva Reserva</a>

    {{-- Botones de exportación --}}
    <a href="{{ route('reservasr.exportExcel') }}" class="btn btn-primary mb-3">Exportar Excel</a>
    <a href="{{ route('reservasr.exportPDF') }}" class="btn btn-danger mb-3">Exportar PDF</a>

    {{-- Mensajes de éxito --}}
    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    {{-- Filtro para mostrar reservas ocultas --}}
    <form method="GET" class="mb-3">
        <label>
            <input type="checkbox" name="mostrar_ocultos" value="1" {{ request('mostrar_ocultos') ? 'checked' : '' }}>
            Mostrar reservas ocultas
        </label>
        <button type="submit" class="btn btn-primary btn-sm">Filtrar</button>
    </form>

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Mesa</th>
                <th>Fecha</th>
                <th>Hora</th>
                <th># Personas</th>
                <th>Estado</th>
                <th>Activo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse($reservas as $reserva)
                <tr>
                    <td>{{ $reserva->id_reserva }}</td>
                    <td>
                        @if($reserva->cliente)
                            {{ $reserva->cliente->nombre }} {{ $reserva->cliente->apellido }}
                        @else
                            <em>Anónimo</em>
                        @endif
                    </td>
                    <td>{{ $reserva->mesa->numero_mesa }}</td>
                    <td>{{ $reserva->fecha_reserva }}</td>
                    <td>{{ $reserva->hora_reserva }}</td>
                    <td>{{ $reserva->numero_personas }}</td>
                    <td>{{ ucfirst($reserva->estado_reserva) }}</td>
                    <td>{{ $reserva->activo ? 'Sí' : 'No' }}</td>
                    <td>
                        <a href="{{ route('reservasr.gestion.show', $reserva->id_reserva) }}" class="btn btn-info btn-sm">Ver</a>
                        <a href="{{ route('reservasr.gestion.edit', $reserva->id_reserva) }}" class="btn btn-warning btn-sm">Editar</a>

                        {{-- Ocultar / Restaurar --}}
                        @if($reserva->activo)
                            <form action="{{ route('reservasr.ocultar', $reserva->id_reserva) }}" method="POST" class="d-inline">
                                @csrf
                                @method('PATCH')
                                <button type="submit" class="btn btn-danger btn-sm">Eliminar</button>
                            </form>
                        @else
                            <form action="{{ route('reservasr.mostrar', $reserva->id_reserva) }}" method="POST" class="d-inline">
                                @csrf
                                @method('PATCH')
                                <button type="submit" class="btn btn-success btn-sm">Restaurar</button>
                            </form>
                        @endif
                    </td>
                </tr>
            @empty
                <tr><td colspan="9">No hay reservas registradas.</td></tr>
            @endforelse
        </tbody>
    </table>
</div>
@endsection
