<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Habitacion;
use App\Models\TipoHabitacion;
use App\Exports\HabitacionesExport;
use Barryvdh\DomPDF\Facade\Pdf;
use Maatwebsite\Excel\Facades\Excel;

class ExportHabitacionController extends Controller
{
    public function index(Request $request)
    {
        $query = Habitacion::with('tipoHabitacion');

        if ($request->filled('estado_habitacion')) {
            $query->where('estado_habitacion', $request->estado_habitacion);
        }

        if ($request->filled('tipo')) {
            $query->where('id_tipo_habitacion', $request->tipo);
        }

        if ($request->filled('desde') && $request->filled('hasta')) {
            $query->whereBetween('created_at', [$request->desde, $request->hasta]);
        }

        $habitaciones = $query->get();
        $tipos = TipoHabitacion::all();

        return view('administrador.habitaciones.reportes', compact('habitaciones', 'tipos'));
    }

    public function exportarExcel(Request $request)
    {
        return Excel::download(new HabitacionesExport($request->all()), 'habitaciones.xlsx');
    }

    public function exportarPDF(Request $request)
    {
        $export = new HabitacionesExport($request->all());
        $habitaciones = $export->query()->get();

        $pdf = Pdf::loadView('administrador.habitaciones.pdf', compact('habitaciones'))
                  ->setPaper('a4', 'landscape');

        return $pdf->download('habitaciones.pdf');
    }
}