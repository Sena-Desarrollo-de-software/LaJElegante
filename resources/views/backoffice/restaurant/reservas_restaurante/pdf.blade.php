<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Listado de Reservas</title>
    <style>
        body { font-family: DejaVu Sans, sans-serif; font-size: 12px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { border: 1px solid #000; padding: 5px; text-align: left; }
        h1 { text-align: center; }
    </style>
</head>
<body>
    <h1>Listado de Reservas</h1>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Cliente</th>
                <th>Mesa</th>
                <th>Fecha</th>
                <th>Hora</th>
                <th># Personas</th>
                <th>Estado</th>
                <th>Activo</th>
            </tr>
        </thead>
        <tbody>
            @foreach($reservas as $reserva)
                <tr>
                    <td>{{ $reserva->id_reserva }}</td>
                    <td>{{ $reserva->cliente->nombre }} {{ $reserva->cliente->apellido }}</td>
                    <td>{{ $reserva->mesa->numero_mesa }}</td>
                    <td>{{ $reserva->fecha_reserva }}</td>
                    <td>{{ $reserva->hora_reserva }}</td>
                    <td>{{ $reserva->numero_personas }}</td>
                    <td>{{ ucfirst($reserva->estado_reserva) }}</td>
                    <td>{{ $reserva->activo ? 'Sí' : 'No' }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
