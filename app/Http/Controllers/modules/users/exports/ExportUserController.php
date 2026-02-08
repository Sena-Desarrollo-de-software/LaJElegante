<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use App\Exports\UsersExport;
use Barryvdh\DomPDF\Facade\Pdf;
use Maatwebsite\Excel\Facades\Excel;

class ExportUserController extends Controller
{
    public function index(Request $request)
    {
        $query = User::query();

        if ($request->filled('role')) {
            $query->where('role', $request->role);
        }

        if ($request->filled('estado')) {
            $query->where('estado', $request->estado);
        }

        if ($request->filled('desde') && $request->filled('hasta')) {
            $query->whereBetween('created_at', [$request->desde, $request->hasta]);
        }

        $usuarios = $query->get();

        $roles = [
            'recepcionista',
            'asistente_administrativo',
            'gerente_alimentos',
            'gerente_habitaciones',
            'gerente_general',
            'administrador',
        ];

        return view('administrador.users.reportes', compact('usuarios', 'roles'));
    }

    public function exportarExcel(Request $request)
    {
        return Excel::download(new UsersExport($request->all()), 'usuarios.xlsx');
    }

    public function exportarPDF(Request $request)
    {
        $export = new UsersExport($request->all());
        $usuarios = $export->query()->get();

        $role = $request->get('role', 'todos');
        $fecha = now()->format('Y-m-d_H-i-s'); 

        $filename = "usuarios_{$role}_{$fecha}.pdf";

        $pdf = Pdf::loadView('administrador.users.pdf', compact('usuarios'))
                ->setPaper('a4', 'landscape');

        return $pdf->download($filename);
    }
}