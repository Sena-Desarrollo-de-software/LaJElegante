<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Listado de Mesas</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { border: 1px solid #000; padding: 5px; text-align: left; }
    </style>
</head>
<body>
    <h1>Listado de Mesas</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Capacidad</th>
                <th>Activo</th>
            </tr>
        </thead>
        <tbody>
            @foreach($mesas as $mesa)
                <tr>
                    <td>{{ $mesa->id_mesa }}</td>
                    <td>{{ $mesa->nombre }}</td>
                    <td>{{ $mesa->capacidad }}</td>
                    <td>{{ $mesa->activo ? 'Sí' : 'No' }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
