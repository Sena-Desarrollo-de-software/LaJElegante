@extends('administrador.layouts.tipo_cliente')

@section('content')
<div class="container">
    <h1 class="mb-4">Papelera de Tipos de Cliente</h1>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    @if($tipos->count())
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre Tipo</th>
                    <th>Eliminado en</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                @foreach($tipos as $tipo)
                <tr>
                    <td>{{ $tipo->id_tipo_cliente }}</td>
                    <td>{{ $tipo->nombre_tipo }}</td>
                    <td>{{ $tipo->deleted_at->format('d/m/Y H:i') }}</td>
                    <td>
                        <form action="{{ route('tipo_cliente.restaurar', $tipo->id_tipo_cliente) }}" method="POST" style="display:inline-block">
                            @csrf
                            @method('PATCH')
                            <button type="submit" class="btn btn-success btn-sm">Restaurar</button>
                        </form>

                    </td>
                </tr>
                @endforeach
            </tbody>
        </table>

        <a href="{{ route('tipo_cliente.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @else
        <div class="alert alert-info">
            No hay tipos de cliente en la papelera.
        </div>
        <a href="{{ route('tipo_cliente.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @endif
</div>
@endsection
