<?php

namespace App\Http\Controllers;

use App\Models\Habitacion;
use App\Models\TipoHabitacion;
use Illuminate\Http\Request;

class HabitacionController extends Controller
{
    public function index()
    {
        $habitaciones = Habitacion::with('tipoHabitacion')->get();
        return view('administrador.habitaciones.index', compact('habitaciones'));
    }

    public function create()
    {
        $tipos = TipoHabitacion::all();
        return view('administrador.habitaciones.create', compact('tipos'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'id_tipo_habitacion' => 'required|exists:tipo_habitacion,id_tipo_habitacion',
            'numero_habitacion' => 'required|string|max:3|unique:habitaciones',
            'estado_habitacion' => 'required|in:en servicio,mantenimiento,inactiva',
        ]);

        Habitacion::create($request->all());

        return redirect()->route('habitaciones.gestion.index')
            ->with('success', 'Habitación creada correctamente.');
    }

    public function update(Request $request, $id)
    {
        $habitacion = Habitacion::findOrFail($id);

        $request->validate([
            'id_tipo_habitacion' => 'required|exists:tipo_habitacion,id_tipo_habitacion',
            'numero_habitacion' => 'required|string|max:3|unique:habitaciones,numero_habitacion,' . $habitacion->id_habitacion . ',id_habitacion',
            'estado_habitacion' => 'required|in:en servicio,mantenimiento,inactiva',
        ]);

        $habitacion->update($request->all());

        return redirect()->route('habitaciones.gestion.index')
            ->with('success', 'Habitación actualizada correctamente.');
    }

    public function destroy($id)
    {
        $habitacion = Habitacion::findOrFail($id);
        $habitacion->delete();

        return redirect()->route('habitaciones.gestion.index')
            ->with('success', 'Habitación eliminada correctamente.');
    }

    public function papelera()
    {
        $habitaciones = Habitacion::onlyTrashed()->with('tipoHabitacion')->get();
        return view('administrador.habitaciones.papelera', compact('habitaciones'));
    }

    public function restaurar($id)
    {
        $habitacion = Habitacion::onlyTrashed()->findOrFail($id);
        $habitacion->restore();

        return redirect()->route('habitaciones.papelera')
            ->with('success', 'Habitación restaurada correctamente.');
    }
}