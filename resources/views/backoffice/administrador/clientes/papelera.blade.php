@extends('administrador.layouts.clientes')

@section('content')
<div class="container">
    <h1 class="mb-4">Papelera de Clientes</h1>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    @if($clientes->count())
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Teléfono</th>
                    <th>Eliminado en</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                @foreach($clientes as $cliente)
                <tr>
                    <td>{{ $cliente->id_cliente }}</td>
                    <td>{{ $cliente->nombre }}</td>
                    <td>{{ $cliente->email_info }}</td>
                    <td>{{ $cliente->numero_telefono }}</td>
                    <td>{{ $cliente->deleted_at->format('d/m/Y H:i') }}</td>
                    <td>
                        {{-- Restaurar --}}
                    <form action="{{ route('clientes.restaurar', $cliente->id_cliente) }}" method="POST" style="display:inline-block">
                        @csrf
                        @method('PATCH')
                        <button type="submit" class="btn btn-success btn-sm">
                            Restaurar
                        </button>
                    </form>
                    </td>
                </tr>
                @endforeach
            </tbody>
        </table>

        <a href="{{ route('clientes.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @else
        <div class="alert alert-info">
            No hay clientes en la papelera.
        </div>
        <a href="{{ route('clientes.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @endif
</div>
@endsection
