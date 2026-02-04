@extends('administrador.layouts.tipo_cliente')

@section('content')
<div class="container mt-4">
    <h1 class="mb-4">Tipos de Cliente</h1>

    {{-- Mensaje de éxito --}}
    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    <a href="{{ route('tipo_cliente.gestion.create') }}" class="btn btn-primary mb-3">
        + Nuevo Tipo de Cliente
    </a>

    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Nombre del Tipo</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse($tipos as $tipo)
                <tr>
                    <td>{{ $tipo->id_tipo_cliente }}</td>
                    <td>{{ $tipo->nombre_tipo }}</td>
                    <td>
                        <button type="button" class="btn btn-sm btn-warning btn-edit" data-id="{{ $tipo->id_tipo_cliente }}" data-nombre="{{ $tipo->nombre_tipo }}">Editar</button>

                        <form action="{{ route('tipo_cliente.gestion.destroy', $tipo) }}" method="POST" style="display:inline-block;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-sm btn-danger"
                                onclick="return confirm('¿Seguro que deseas eliminar este tipo de cliente?')">
                                Eliminar
                            </button>
                        </form>
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="3" class="text-center">No hay tipos de cliente registrados</td>
                </tr>
            @endforelse
        </tbody>
    </table>
</div>
<!-- Modal Editar Tipo de Cliente -->
<div class="modal fade" id="editModal" tabindex="-1" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <form method="POST">
                @csrf
                @method('PUT')
                <div class="modal-header">
                    <h5 class="modal-title">Editar Tipo de Cliente</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Cerrar"></button>
                </div>
                <div class="modal-body">
                    <div class="mb-3">
                        <label class="form-label">Nombre del Tipo</label>
                        <input type="text" name="nombre_tipo" class="form-control" required>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                    <button type="submit" class="btn btn-success">Guardar Cambios</button>
                </div>
            </form>
        </div>
    </div>
</div>
@endsection