<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Carbon\Carbon;

class DashboardController extends Controller
{
    public function index()
{
    $hoy = \Carbon\Carbon::today();

    $clientesCount     = \App\Models\Cliente::count();
    $usuariosCount     = \App\Models\User::count();
    $habitacionesCount = \App\Models\Habitacion::count();

    $reservasActivas = \App\Models\DetalleReservaHabitacion::whereDate('fecha_inicio', '<=', $hoy)
        ->whereDate('fecha_fin', '>=', $hoy)
        ->count();

    $reservasQuery = \App\Models\ReservaHabitacion::selectRaw('MONTH(created_at) as mes, COUNT(*) as total')
        ->whereYear('created_at', now()->year)
        ->groupBy('mes')
        ->pluck('total', 'mes')
        ->toArray();

    $mesesLabels = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
    $reservasPorMes = [];
    for ($i = 1; $i <= 12; $i++) {
        $reservasPorMes[] = $reservasQuery[$i] ?? 0;
    }

    $ocupadas = \App\Models\DetalleReservaHabitacion::whereDate('fecha_inicio', '<=', $hoy)
        ->whereDate('fecha_fin', '>=', $hoy)
        ->count();
    $disponibles = max($habitacionesCount - $ocupadas, 0);
    $ocupacion = [$ocupadas, $disponibles];

    return view('administrador.dashboard.index', compact(
        'clientesCount',
        'usuariosCount',
        'habitacionesCount',
        'reservasActivas',
        'mesesLabels',
        'reservasPorMes',
        'ocupacion'
    ));
}
}