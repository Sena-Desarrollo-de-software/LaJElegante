<?php

namespace App\Http\Controllers;

use App\Models\Tarifa;
use App\Models\Temporada;
use Illuminate\Http\Request;

class TarifaController extends Controller
{
    public function index()
    {
        $tarifas = Tarifa::with('temporada')->get();
        return view('administrador.tarifas.index', compact('tarifas'));
    }

    public function create()
    {
        $temporadas = Temporada::all();
        return view('administrador.tarifas.create', compact('temporadas'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'tarifa_fija' => 'required|numeric|min:0',
            'precio_final' => 'required|numeric|min:0',
            'estado' => 'required|in:vigente,inactiva',
            'id_temporada' => 'required|exists:temporadas,id_temporada',
        ]);

        Tarifa::create($request->all());
        return redirect()->route('tarifas.gestion.index')->with('success', 'Tarifa creada correctamente.');
    }

 /*   public function edit($id)
    {
        $tarifa = Tarifa::findOrFail($id);
        $temporadas = Temporada::all();
        return view('tarifas.gestion.edit', compact('tarifa', 'temporadas'));
    }
*/
    public function update(Request $request, $id)
    {
        $tarifa = Tarifa::findOrFail($id);

        $request->validate([
            'tarifa_fija' => 'required|numeric|min:0',
            'precio_final' => 'required|numeric|min:0',
            'estado' => 'required|in:vigente,inactiva',
            'id_temporada' => 'required|exists:temporadas,id_temporada',
        ]);

        $tarifa->update($request->all());
        return redirect()->route('tarifas.gestion.index')->with('success', 'Tarifa actualizada correctamente.');
    }

    public function destroy($id)
    {
        $tarifa = Tarifa::findOrFail($id);
        $tarifa->delete();
        return redirect()->route('tarifas.gestion.index')->with('success', 'Tarifa eliminada (soft delete).');
    }

    // Soft deletes
    public function papelera()
    {
        $tarifas = Tarifa::onlyTrashed()->with('temporada')->get();
        return view('administrador.tarifas.papelera', compact('tarifas'));
    }

    public function restaurar($id)
    {
        $tarifa = Tarifa::onlyTrashed()->findOrFail($id);
        $tarifa->restore();
        return redirect()->route('tarifas.papelera')->with('success', 'Tarifa restaurada correctamente.');
    }
    
    public function getTarifaPorHabitacion($idHabitacion)
    {
        $habitacion = \App\Models\Habitacion::with('tipoHabitacion')->find($idHabitacion);

        if (! $habitacion) {
            return response()->json(['error' => 'Habitación no encontrada'], 404);
        }

        $tarifa = \App\Models\Tarifa::where('id_tipo_habitacion', $habitacion->id_tipo_habitacion)
            ->where('estado', 'vigente')
            ->orderByDesc('id_tarifa') 
            ->first();

        return response()->json([
            'tarifa_fija'      => $tarifa->tarifa_fija ?? '0.00',
            'precio_final'     => $tarifa->precio_final ?? '0.00',
            'id_tarifa'        => $tarifa->id_tarifa ?? null,
            'capacidad_maxima' => $habitacion->tipoHabitacion->capacidad_maxima ?? null,
            'tipo_nombre'      => $habitacion->tipoHabitacion->nombre_tipo ?? null,
        ]);
    }
}