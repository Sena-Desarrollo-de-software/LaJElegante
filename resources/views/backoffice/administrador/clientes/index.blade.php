@extends('administrador.layouts.clientes')

@section('content')
<div class="container">
    <h1>Listado de Clientes</h1>

    <a href="{{ route('clientes.gestion.create') }}" class="btn btn-primary mb-3">Nuevo Cliente</a>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    <table class="table table-bordered">
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre completo</th>
                <th>Email</th>
                <th>Telefono</th>
                <th>Tipo Cliente</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
        @foreach($clientes as $cliente)
            <tr>
                <td>{{ $cliente->id_cliente }}</td>
                <td>{{ $cliente->nombre }} {{ $cliente->apellido }}</td>
                <td>{{ $cliente->email_info }}</td>
                <td>{{ $cliente->numero_telefono }}</td>
                <td>{{ $cliente->tipoCliente->nombre_tipo ?? 'Sin tipo' }}</td>
                <td>{{ ucfirst($cliente->estado) }}</td>
                <td>
                    <a href="{{ route('clientes.gestion.show', $cliente->id_cliente) }}" class="btn btn-info btn-sm">Ver</a>
                    <a href="{{ route('clientes.gestion.edit', $cliente->id_cliente) }}" class="btn btn-warning btn-sm">Editar</a>
                    <form action="{{ route('clientes.gestion.destroy', $cliente->id_cliente) }}" method="POST" style="display:inline-block">
                        @csrf
                        @method('DELETE')
                        <button type="submit" class="btn btn-danger btn-sm"
                                onclick="return confirm('¿Seguro que deseas eliminar este cliente?')">
                                Eliminar
                        </button>
                    </form>
                </td>
            </tr>
        @endforeach
        </tbody>
    </table>
</div>
@endsection