@extends('administrador.layouts.tipo_habitacion')

@section('content')
<div class="d-flex justify-content-between mb-3">
    <h2>Listado de Tipos de Habitación</h2>
    <a href="{{ route('tipo_habitacion.gestion.create') }}" class="btn btn-success">+ Nuevo</a>
</div>

@if(session('success'))
    <div class="alert alert-success">{{ session('success') }}</div>
@endif

<table class="table table-striped table-bordered">
    <thead class="table-dark">
        <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Descripción</th>
            <th>Capacidad</th>
            <th>Acciones</th>
        </tr>
    </thead>
    <tbody>
        @forelse($tipos as $tipo)
            <tr>
                <td>{{ $tipo->id_tipo_habitacion }}</td>
                <td>{{ ucfirst($tipo->nombre_tipo) }}</td>
                <td>{{ $tipo->descripcion }}</td>
                <td>{{ $tipo->capacidad_maxima }}</td>
                <td>
                    <!-- Botón para abrir modal -->
                    <button class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#editModal{{ $tipo->id_tipo_habitacion }}">
                        Editar
                    </button>

                    <!-- Formulario eliminar -->
                    <form action="{{ route('tipo_habitacion.gestion.destroy', $tipo->id_tipo_habitacion) }}" method="POST" class="d-inline">
                        @csrf
                        @method('DELETE')
                        <button class="btn btn-danger btn-sm" onclick="return confirm('¿Seguro que deseas eliminar este tipo de habitación?')">Eliminar</button>
                    </form>
                </td>
            </tr>

            <!-- Modal de edición -->
            <div class="modal fade" id="editModal{{ $tipo->id_tipo_habitacion }}" tabindex="-1" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <form action="{{ route('tipo_habitacion.gestion.update', $tipo->id_tipo_habitacion) }}" method="POST">
                            @csrf
                            @method('PUT')

                            <div class="modal-header">
                                <h5 class="modal-title">Editar Tipo de Habitación</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>

                            <div class="modal-body">
                                <div class="mb-3">
                                    <label class="form-label">Nombre</label>
                                    <select name="nombre_tipo" class="form-select" required>
                                        <option value="familiar" {{ $tipo->nombre_tipo == 'familiar' ? 'selected' : '' }}>Familiar</option>
                                        <option value="pareja" {{ $tipo->nombre_tipo == 'pareja' ? 'selected' : '' }}>Pareja</option>
                                        <option value="basica" {{ $tipo->nombre_tipo == 'basica' ? 'selected' : '' }}>Básica</option>
                                        <option value="especial" {{ $tipo->nombre_tipo == 'especial' ? 'selected' : '' }}>Especial</option>
                                    </select>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Descripción</label>
                                    <textarea name="descripcion" class="form-control" rows="3">{{ $tipo->descripcion }}</textarea>
                                </div>

                                <div class="mb-3">
                                    <label class="form-label">Capacidad Máxima</label>
                                    <input type="number" name="capacidad_maxima" class="form-control" value="{{ $tipo->capacidad_maxima }}" required>
                                </div>
                            </div>

                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="submit" class="btn btn-primary">Guardar Cambios</button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>

        @empty
            <tr>
                <td colspan="5" class="text-center">No hay tipos de habitación registrados</td>
            </tr>
        @endforelse
    </tbody>
</table>
@endsection