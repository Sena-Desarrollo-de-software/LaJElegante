<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Cliente;
use App\Models\TipoCliente;
use App\Exports\ClientesExport;
use Barryvdh\DomPDF\Facade\Pdf;
use Maatwebsite\Excel\Facades\Excel;

class ExportClienteController extends Controller
{
    public function index(Request $request)
    {
        $query = Cliente::query();

        if ($request->filled('estado')) {
            $query->where('estado', $request->estado);
        }

        if ($request->filled('tipo')) {
            $query->where('id_tipo_cliente', $request->tipo);
        }

        if ($request->filled('desde') && $request->filled('hasta')) {
            $query->whereBetween('created_at', [$request->desde, $request->hasta]);
        }

        $clientes = $query->get();
        $tipos = TipoCliente::all();

        return view('administrador.clientes.reportes', compact('clientes', 'tipos'));
    }
        public function exportarExcel(Request $request)
    {
        return Excel::download(new ClientesExport($request->all()), 'clientes.xlsx');
    }

    public function exportarPDF(Request $request)
    {
        $export = new ClientesExport($request->all());
        $clientes = $export->query()->get();

        $tipo = $request->get('tipo', 'todos');
        $estado = $request->get('estado', 'todos');
        $fecha = now()->format('Y-m-d_H-i-s'); 

        $filename = "clientes_{$tipo}_{$estado}_{$fecha}.pdf";

        $pdf = Pdf::loadView('administrador.clientes.pdf', compact('clientes'))
                ->setPaper('a4', 'landscape');

        return $pdf->download($filename);
    }
}