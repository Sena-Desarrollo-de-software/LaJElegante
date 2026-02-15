<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Clientes</title>
    <style>
        body { font-family: DejaVu Sans, sans-serif; font-size: 12px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #000; padding: 6px; text-align: left; }
        th { background: #f2f2f2; }
        h2 { text-align: center; margin-bottom: 20px; }
    </style>
</head>
<body>
    <h2>Reporte de Clientes</h2>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre completo</th>
                <th>Email</th>
                <th>Tipo Cliente</th>
                <th>Estado</th>
                <th>Creado</th>
            </tr>
        </thead>
        <tbody>
            @foreach($clientes as $cliente)
            <tr>
                <td>{{ $cliente->id_cliente }}</td>
                <td>{{ $cliente->nombre }} {{ $cliente->apellido }}</td>
                <td>{{ $cliente->email_info }}</td>
                <td>{{ $cliente->tipoCliente->nombre_tipo ?? 'Sin tipo' }}</td>
                <td>{{ ucfirst($cliente->estado) }}</td>
                <td>{{ $cliente->created_at->format('d/m/Y') }}</td>
            </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>