@extends('administrador.layouts.temporadas')

@section('content')
<h2>Listado de Temporadas</h2>

@if(session('success'))
<div class="alert alert-success">{{ session('success') }}</div>
@endif

<table class="table table-bordered">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Inicio</th>
            <th>Fin</th>
            <th>Modificador</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        @forelse($temporadas as $temporada)
        <tr>
            <td>{{ $temporada->id_temporada }}</td>
            <td>{{ ucfirst($temporada->nombre) }}</td>
            <td>{{ $temporada->fecha_inicio }}</td>
            <td>{{ $temporada->fecha_fin }}</td>
            <td>{{ $temporada->modificador_precio }}%</td>
            <td>
                <!-- Botón Editar (abre modal) -->
                <button class="btn btn-primary btn-sm" data-bs-toggle="modal" data-bs-target="#editModal{{ $temporada->id_temporada }}">
                    Editar
                </button>

                <!-- Botón Eliminar -->
                <form action="{{ route('temporadas.gestion.destroy', $temporada->id_temporada) }}" method="POST" class="d-inline">
                    @csrf
                    @method('DELETE')
                    <button class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar esta temporada?')">Eliminar</button>
                </form>
            </td>
        </tr>

        <!-- Modal de edición -->
        <div class="modal fade" id="editModal{{ $temporada->id_temporada }}" tabindex="-1">
            <div class="modal-dialog">
                <div class="modal-content">
                    <form action="{{ route('temporadas.gestion.update', $temporada->id_temporada) }}" method="POST">
                        @csrf
                        @method('PUT')
                        <div class="modal-header">
                            <h5 class="modal-title">Editar Temporada</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <div class="mb-3">
                                <label for="nombre" class="form-label">Nombre</label>
                                <select name="nombre" class="form-control" required>
                                    <option value="alta" {{ $temporada->nombre == 'alta' ? 'selected' : '' }}>Alta</option>
                                    <option value="media" {{ $temporada->nombre == 'media' ? 'selected' : '' }}>Media</option>
                                    <option value="baja" {{ $temporada->nombre == 'baja' ? 'selected' : '' }}>Baja</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Fecha inicio</label>
                                <input type="date" name="fecha_inicio" class="form-control" value="{{ $temporada->fecha_inicio }}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Fecha fin</label>
                                <input type="date" name="fecha_fin" class="form-control" value="{{ $temporada->fecha_fin }}" required>
                            </div>
                            <div class="mb-3">
                                <label class="form-label">Modificador precio (%)</label>
                                <input type="number" step="0.01" name="modificador_precio" class="form-control" value="{{ $temporada->modificador_precio }}" required>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button class="btn btn-primary">Guardar cambios</button>
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
        @empty
        <tr><td colspan="6" class="text-center">No hay temporadas registradas</td></tr>
        @endforelse
    </tbody>
</table>
@endsection