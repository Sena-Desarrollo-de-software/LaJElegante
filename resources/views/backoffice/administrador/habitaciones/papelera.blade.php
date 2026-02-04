@extends('administrador.layouts.habitaciones')

@section('content')
    <h1 class="mb-4">Papelera de Habitaciones</h1>

    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>#</th>
                <th>Número</th>
                <th>Tipo</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse($habitaciones as $habitacion)
                <tr>
                    <td>{{ $habitacion->id_habitacion }}</td>
                    <td>{{ $habitacion->numero_habitacion }}</td>
                    <td>{{ $habitacion->tipoHabitacion->nombre_tipo ?? 'N/A' }}</td>
                    <td>{{ ucfirst($habitacion->estado_habitacion) }}</td>
                    <td>
                        <form action="{{ route('habitaciones.restaurar', $habitacion->id_habitacion) }}" method="POST" class="d-inline">
                            @csrf
                            @method('PATCH')
                            <button type="submit" class="btn btn-success btn-sm">Restaurar</button>
                        </form>
                    </td>
                </tr>
            @empty
                <tr><td colspan="5" class="text-center">No hay habitaciones en la papelera.</td></tr>
            @endforelse
        </tbody>
    </table>

    <a href="{{ route('habitaciones.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
@endsection