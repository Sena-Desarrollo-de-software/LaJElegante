<?php

namespace App\Http\Controllers;

use App\Models\TipoHabitacion;
use Illuminate\Http\Request;

class TipoHabitacionController extends Controller
{
    public function index()
    {
        $tipos = TipoHabitacion::all();
        return view('administrador.tipo_habitacion.index', compact('tipos'));
    }

    public function create()
    {
        return view('administrador.tipo_habitacion.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombre_tipo' => 'required|in:familiar,pareja,basica,especial',
            'descripcion' => 'nullable|string|max:500',
            'capacidad_maxima' => 'required|integer|min:1',
        ]);

        TipoHabitacion::create($request->all());

        return redirect()->route('tipo_habitacion.gestion.index')
                         ->with('success', 'Tipo de habitación creado correctamente.');
    }

/*    public function edit(TipoHabitacion $tipoHabitacion)
    {
        return view('tipo_habitacion.gestion.edit', compact('tipoHabitacion'));
    }
*/
    public function update(Request $request, TipoHabitacion $tipoHabitacion)
    {
        $request->validate([
            'nombre_tipo' => 'required|in:familiar,pareja,basica,especial',
            'descripcion' => 'nullable|string|max:500',
            'capacidad_maxima' => 'required|integer|min:1',
        ]);

        $tipoHabitacion->update($request->all());

        return redirect()->route('tipo_habitacion.gestion.index')
                         ->with('success', 'Tipo de habitación actualizado correctamente.');
    }

    public function destroy(TipoHabitacion $tipoHabitacion)
    {
        $tipoHabitacion->delete();

        return redirect()->route('tipo_habitacion.gestion.index')
                         ->with('success', 'Tipo de habitación eliminado correctamente.');
    }

    
    public function papelera()
    {
        $tipos = TipoHabitacion::onlyTrashed()->get();
        return view('administrador.tipo_habitacion.papelera', compact('tipos'));
    }

    
    public function restaurar($id)
    {
        $tipo = TipoHabitacion::withTrashed()->findOrFail($id);
        $tipo->restore();

        return redirect()->route('tipo_habitacion.papelera')
                         ->with('success', 'Tipo de habitación restaurado correctamente.');
    }
}
