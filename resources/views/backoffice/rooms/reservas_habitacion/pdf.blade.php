<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Reporte de Reservas</title>
    <style>
        body { font-family: DejaVu Sans, sans-serif; font-size: 12px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #000; padding: 5px; text-align: center; }
        th { background: #f0f0f0; }
        h2 { text-align: center; }
    </style>
</head>
<body>
    <h2>Reporte de Reservas de Habitaciones</h2>

    <table>
        <thead>
            <tr>
                <th>Cliente</th>
                <th>Habitación</th>
                <th>Fechas</th>
                <th>Noches</th>
                <th>Precio Total</th>
                <th>Observaciones</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($reservas as $r)
                <tr>
                    <td>{{ $r->cliente->nombre }} {{ $r->cliente->apellido }}</td>
                    <td>{{ $r->detalle->habitacion->numero_habitacion }}</td>
                    <td>{{ $r->detalle->fecha_inicio }} - {{ $r->detalle->fecha_fin }}</td>
                    <td>{{ $r->detalle->noches }}</td>
                    <td>${{ number_format($r->detalle->precio_reserva, 2) }}</td>
                    <td>{{ $r->detalle->observaciones ?? '-' }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>