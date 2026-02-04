@extends('administrador.layouts.tarifas')

@section('content')
    <h1 class="mb-4">Listado de Tarifas</h1>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    <a href="{{ route('tarifas.gestion.create') }}" class="btn btn-primary mb-3">Nueva tarifa</a>

    <table class="table table-bordered table-striped">
        <thead class="table-dark">
            <tr>
                <th>ID</th>
                <th>Tarifa fija</th>
                <th>Precio final</th>
                <th>Estado</th>
                <th>Temporada</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            @forelse($tarifas as $tarifa)
                <tr>
                    <td>{{ $tarifa->id_tarifa }}</td>
                    <td>{{ $tarifa->tarifa_fija }}</td>
                    <td>{{ $tarifa->precio_final }}</td>
                    <td>{{ ucfirst($tarifa->estado) }}</td>
                    <td>{{ $tarifa->temporada->nombre ?? 'N/A' }}</td>
                    <td>
                        <!-- Botón editar (abre modal) -->
                        <button class="btn btn-warning btn-sm" data-bs-toggle="modal" data-bs-target="#editModal{{ $tarifa->id_tarifa }}">Editar</button>

                        <!-- Botón eliminar -->
                        <form action="{{ route('tarifas.gestion.destroy', $tarifa) }}" method="POST" class="d-inline">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger btn-sm" onclick="return confirm('¿Eliminar esta tarifa?')">Eliminar</button>
                        </form>
                    </td>
                </tr>

                <!-- Modal de edición -->
                <div class="modal fade" id="editModal{{ $tarifa->id_tarifa }}" tabindex="-1" aria-hidden="true">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <form action="{{ route('tarifas.gestion.update', $tarifa) }}" method="POST">
                                @csrf
                                @method('PUT')
                                <div class="modal-header">
                                    <h5 class="modal-title">Editar tarifa</h5>
                                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                                </div>
                                <div class="modal-body">
                                    <div class="mb-3">
                                        <label>Tarifa fija</label>
                                        <input type="number" step="0.01" name="tarifa_fija" class="form-control" value="{{ $tarifa->tarifa_fija }}" required>
                                    </div>
                                    <div class="mb-3">
                                        <label>Precio final</label>
                                        <input type="number" step="0.01" name="precio_final" class="form-control" value="{{ $tarifa->precio_final }}" required>
                                    </div>
                                    <div class="mb-3">
                                        <label>Estado</label>
                                        <select name="estado" class="form-select">
                                            <option value="vigente" @if($tarifa->estado == 'vigente') selected @endif>Vigente</option>
                                            <option value="inactiva" @if($tarifa->estado == 'inactiva') selected @endif>Inactiva</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label>Temporada</label>
                                        <select name="id_temporada" class="form-select">
                                            @foreach(\App\Models\Temporada::all() as $temporada)
                                                <option value="{{ $temporada->id_temporada }}" @if($tarifa->id_temporada == $temporada->id_temporada) selected @endif>
                                                    {{ ucfirst($temporada->nombre) }}
                                                </option>
                                            @endforeach
                                        </select>
                                    </div>
                                </div>
                                <div class="modal-footer">
                                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                    <button type="submit" class="btn btn-success">Actualizar</button>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            @empty
                <tr>
                    <td colspan="6" class="text-center">No hay tarifas registradas.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
@endsection
