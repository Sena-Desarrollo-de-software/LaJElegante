@extends('administrador.layouts.users')

@section('content')
<div class="container">
    <h1 class="mb-4">Papelera de Usuarios</h1>

    @if(session('success'))
        <div class="alert alert-success">{{ session('success') }}</div>
    @endif

    @if($usuarios->count())
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nombre</th>
                    <th>Email</th>
                    <th>Rol</th>
                    <th>Eliminado en</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                @foreach($usuarios as $usuario)
                <tr>
                    <td>{{ $usuario->id }}</td>
                    <td>{{ $usuario->name }}</td>
                    <td>{{ $usuario->email }}</td>
                    <td>{{ ucfirst(str_replace('_',' ', $usuario->role)) }}</td>
                    <td>{{ $usuario->deleted_at->format('d/m/Y H:i') }}</td>
                    <td>
                        {{-- Restaurar --}}
                        <form action="{{ route('users.restaurar', $usuario->id) }}" method="POST" style="display:inline-block">
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

        <a href="{{ route('users.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @else
        <div class="alert alert-info">
            No hay usuarios en la papelera.
        </div>
        <a href="{{ route('users.gestion.index') }}" class="btn btn-secondary">Volver al listado</a>
    @endif
</div>
@endsection