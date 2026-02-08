<?php

namespace App\Http\Controllers;

use App\Models\ReservaHabitacion;
use App\Models\TipoCliente;
use Illuminate\Http\Request;
use Barryvdh\DomPDF\Facade\Pdf;
use Maatwebsite\Excel\Facades\Excel;
use App\Exports\ReservaHabitacionExport;

class ExportReservaHabitacionController extends Controller
{
    public function index(Request $request)
    {
        $query = ReservaHabitacion::with(['cliente.tipoCliente', 'detalle.habitacion']);

        if ($request->filled('tipo')) {
            if ($request->tipo === 'no_reg') {
                // reservas sin cliente (no registrado)
                $query->whereNull('id_cliente');
            } else {
                $query->whereHas('cliente', function ($q) use ($request) {
                    $q->where('id_tipo_cliente', $request->tipo);
                });
            }
        }

        if ($request->filled('desde') && $request->filled('hasta')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->whereBetween('fecha_inicio', [$request->desde, $request->hasta]);
            });
        }

        if ($request->filled('noches_min')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->where('noches', '>=', $request->noches_min);
            });
        }
        if ($request->filled('noches_max')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->where('noches', '<=', $request->noches_max);
            });
        }

        if ($request->filled('personas_min')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->where('cantidad_personas', '>=', $request->personas_min);
            });
        }
        if ($request->filled('personas_max')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->where('cantidad_personas', '<=', $request->personas_max);
            });
        }

        $reservas = $query->get();

        $tipos = TipoCliente::all();

        $tipos->push((object)[
            'id_tipo_cliente' => 'no_reg',
            'nombre_tipo' => 'No registrado'
        ]);

        return view('administrador.reservash.reportes', compact('reservas', 'tipos'));
    }

    public function exportarExcel(Request $request)
    {
        return Excel::download(new ReservaHabitacionExport($request->all()), 'reservas.xlsx');
    }

    public function exportarPDF(Request $request)
    {
        $export = new ReservaHabitacionExport($request->all());
        $query = ReservaHabitacion::with(['cliente', 'detalle.habitacion']);

        if ($request->filled('cliente')) {
            $query->where('id_cliente', $request->cliente);
        }

        if ($request->filled('desde') && $request->filled('hasta')) {
            $query->whereHas('detalle', function ($q) use ($request) {
                $q->whereBetween('fecha_inicio', [$request->desde, $request->hasta]);
            });
        }

        $reservas = $query->get();
        $fecha = now()->format('Y-m-d_H-i-s');
        $filename = "reservas_{$fecha}.pdf";

        $pdf = Pdf::loadView('administrador.reservas.pdf', compact('reservas'))
                    ->setPaper('a4', 'landscape');

        return $pdf->download($filename);
    }
}