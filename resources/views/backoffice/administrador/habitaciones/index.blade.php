@extends('administrador.layouts.habitaciones')

@section('content')
    <h1 class="mb-4">Listado de Habitaciones</h1>

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
                        <!-- Botón para abrir modal de edición -->
                        <button class="btn btn-warning btn-sm" data-bs-toggle="modal"
                                data-bs-target="#editModal{{ $habitacion->id_habitacion }}">
                            Editar
                        </button>

                        <!-- Eliminar -->
                        <form action="{{ route('habitaciones.gestion.destroy', $habitacion->id_habitacion) }}"
                              method="POST" class="d-inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger btn-sm"
                                    onclick="return confirm('¿Eliminar esta habitación?')">
                                Eliminar
                            </button>
                        </form>
                    </td>
                </tr>

                <!-- Modal de edición -->
                <div class="modal fade" id="editModal{{ $habitacion->id_habitacion }}" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <form action="{{ route('habitaciones.gestion.update', $habitacion->id_habitacion) }}" method="POST">
                                @csrf
                                @method('PUT')
                                <div class="modal-header">
                                    <h5 class="modal-title">Editar Habitación</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <label class="form-label">Número</label>
                                        <input type="text" name="numero_habitacion"
                                               class="form-control"
                                               value="{{ $habitacion->numero_habitacion }}">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Tipo</label>
                                        <select name="id_tipo_habitacion" class="form-select">
                                            @foreach(\App\Models\TipoHabitacion::all() as $tipo)
                                                <option value="{{ $tipo->id_tipo_habitacion }}"
                                                    {{ $habitacion->id_tipo_habitacion == $tipo->id_tipo_habitacion ? 'selected' : '' }}>
                                                    {{ $tipo->nombre_tipo }}
                                                </option>
                                            @endforeach
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Estado</label>
                                        <select name="estado_habitacion" class="form-select">
                                            <option {{ $habitacion->estado_habitacion == 'en servicio' ? 'selected' : '' }}>en servicio</option>
                                            <option {{ $habitacion->estado_habitacion == 'mantenimiento' ? 'selected' : '' }}>mantenimiento</option>
                                            <option {{ $habitacion->estado_habitacion == 'inactiva' ? 'selected' : '' }}>inactiva</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="submit" class="btn btn-primary">Guardar cambios</button>
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            @empty
                <tr><td colspan="5" class="text-center">No hay habitaciones registradas.</td></tr>
            @endforelse
        </tbody>
    </table>
@endsection