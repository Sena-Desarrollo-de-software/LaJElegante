<?php

namespace App\Http\Controllers;

use App\Models\Temporada;
use Illuminate\Http\Request;

class TemporadaController extends Controller
{
    public function index()
    {
        $temporadas = Temporada::all();
        return view('administrador.temporadas.index', compact('temporadas'));
    }

    public function create()
    {
        return view('administrador.temporadas.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombre' => 'required|in:alta,media,baja',
            'fecha_inicio' => 'required|date',
            'fecha_fin' => 'required|date|after_or_equal:fecha_inicio',
            'modificador_precio' => 'required|numeric',
        ]);

        Temporada::create($request->all());

        return redirect()->route('temporadas.gestion.index')->with('success', 'Temporada creada correctamente.');
    }

/*   public function show(Temporada $temporada)
    {
        return view('temporadas.gestion.index', compact('temporada'));
    }

    public function edit(Temporada $temporada)
    {
        return view('temporadas.gestion.index', compact('temporada'));
    }
*/
    public function update(Request $request, Temporada $temporada)
    {
        $request->validate([
            'nombre' => 'required|in:alta,media,baja',
            'fecha_inicio' => 'required|date',
            'fecha_fin' => 'required|date|after_or_equal:fecha_inicio',
            'modificador_precio' => 'required|numeric',
        ]);

        $temporada->update($request->all());

        return redirect()->route('temporadas.gestion.index')->with('success', 'Temporada actualizada correctamente.');
    }

    public function destroy(Temporada $temporada)
    {
        $temporada->delete();
        return redirect()->route('temporadas.gestion.index')->with('success', 'Temporada eliminada correctamente.');
    }

    // SoftDeletes
    public function papelera()
    {
        $temporadas = Temporada::onlyTrashed()->get();
        return view('administrador.temporadas.papelera', compact('temporadas'));
    }

    public function restaurar($id)
    {
        $temporada = Temporada::onlyTrashed()->findOrFail($id);
        $temporada->restore();

        return redirect()->route('temporadas.gestion.index')->with('success', 'Temporada restaurada correctamente.');
    }
}