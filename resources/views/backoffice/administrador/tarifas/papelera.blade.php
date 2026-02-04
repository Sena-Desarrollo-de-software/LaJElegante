@extends('administrador.layouts.tarifas')

@section('content')
    <h1 class="mb-4">Papelera de Tarifas</h1>

   
    @if(session('success'))
        <div class="alert alert-success">
            {{ session('success') }}
        </div>
        <script>
            window.location.href = "{{ route('tarifas.papelera') }}";
        </script>
    @endif

    <a href="{{ route('tarifas.gestion.index') }}" class="btn btn-secondary mb-3">Volver al listado</a>

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
                        <form action="{{ route('tarifas.restaurar', $tarifa->id_tarifa) }}" method="POST" class="d-inline">
                            @csrf
                            @method('PATCH')
                            <button type="submit" class="btn btn-success btn-sm">Restaurar</button>
                        </form>
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="6" class="text-center">No hay tarifas en la papelera.</td>
                </tr>
            @endforelse
        </tbody>
    </table>
@endsection