<?php

namespace App\Http\Controllers;

use App\Models\TipoCliente;
use Illuminate\Http\Request;

class TipoClienteController extends Controller
{
    public function index()
    {
        $tipos = TipoCliente::all();
        return view('administrador.tipo_cliente.index', compact('tipos'));
    }

    public function create()
    {
        return view('administrador.tipo_cliente.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombre_tipo' => 'required|string|max:255',
        ]);

        TipoCliente::create($request->all());

        return redirect()->route('tipo_cliente.gestion.index')
                         ->with('success', 'Tipo de cliente creado correctamente.');
    }

 /*   public function show(TipoCliente $tipo_cliente)
    {
        return view('tipo_cliente.show', compact('tipo_cliente'));
    }

    public function edit(TipoCliente $tipo_cliente)
    {
        return view('tipo_cliente.edit', compact('tipo_cliente'));
    }
*/
    public function update(Request $request, TipoCliente $tipo_cliente)
    {
        $request->validate([
            'nombre_tipo' => 'required|string|max:255',
        ]);

        $tipo_cliente->update($request->all());

        return redirect()->route('tipo_cliente.gestion.index')
                         ->with('success', 'Tipo de cliente actualizado correctamente.');
    }

    public function destroy(TipoCliente $tipo_cliente)
    {
        $tipo_cliente->delete(); 
        return redirect()->route('tipo_cliente.gestion.index')
                         ->with('success', 'Tipo de cliente eliminado correctamente.');
    }

    public function papelera()
    {
        $tipos = TipoCliente::onlyTrashed()->get();
        return view('administrador.tipo_cliente.papelera', compact('tipos'));
    }

    public function restaurar($id)
    {
        $tipo = TipoCliente::withTrashed()->findOrFail($id);
        $tipo->restore();
        return redirect()->route('tipo_cliente.papelera')
                        ->with('success', 'Tipo de cliente restaurado correctamente.');
    }
}