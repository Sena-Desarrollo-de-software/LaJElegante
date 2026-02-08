<?php

namespace App\Http\Controllers;

use App\Models\ReservaHabitacion;
use App\Models\DetalleReservaHabitacion;
use App\Models\Cliente;
use App\Models\Habitacion;
use Illuminate\Http\Request;
use Carbon\Carbon;

class ReservaHabitacionController extends Controller
{
    public function index()
    {
        $reservas = ReservaHabitacion::with(['cliente', 'detalle.habitacion'])->get();
        return view('administrador.reservash.index', compact('reservas'));
    }

    public function create()
    {
        $clientes = Cliente::all();
        $habitaciones = Habitacion::all();
        return view('administrador.reservash.create', compact('clientes', 'habitaciones'));
    }

    public function store(Request $request)
    {
        $request->validate([
            'id_cliente' => 'required|exists:clientes,id_cliente',
            'id_habitacion' => 'required|exists:habitaciones,id_habitacion',
            'fecha_inicio' => 'required|date',
            'fecha_fin' => 'required|date|after:fecha_inicio',
            'cantidad_personas' => 'required|integer|min:1',
            'precio_noche' => 'required|numeric|min:0',
            'descuento_aplicado' => 'nullable|numeric|min:0',
            'recargo_aplicado' => 'nullable|numeric|min:0',
        ]);

        // Calcular noches con Carbon
        $inicio = Carbon::parse($request->fecha_inicio);
        $fin = Carbon::parse($request->fecha_fin);
        $noches = $inicio->diffInDays($fin);

        // Calcular precio base
        $total = ($request->precio_noche * $request->cantidad_personas) * $noches;

        // Aplicar descuento si existe
        if ($request->filled('descuento_aplicado')) {
            $total -= ($total * $request->descuento_aplicado / 100);
        }

        // Aplicar recargo si existe
        if ($request->filled('recargo_aplicado')) {
            $total += ($total * $request->recargo_aplicado / 100);
        }
        // validacion cantitdad de personas
            $habitacion = \App\Models\Habitacion::with('tipoHabitacion')->findOrFail($request->id_habitacion);

        if ($request->cantidad_personas > $habitacion->tipoHabitacion->capacidad_maxima) {
            return back()->withErrors([
                'cantidad_personas' => 'La habitación seleccionada solo admite hasta ' 
                    . $habitacion->tipoHabitacion->capacidad_maxima . ' personas.'
            ])->withInput();
        }
        $detalle = DetalleReservaHabitacion::create([
            'id_habitacion' => $request->id_habitacion,
            'fecha_inicio' => $request->fecha_inicio,
            'fecha_fin' => $request->fecha_fin,
            'cantidad_personas' => $request->cantidad_personas,
            'noches' => $noches,
            'precio_noche' => $request->precio_noche,
            'descuento_aplicado' => $request->descuento_aplicado ?? 0,
            'recargo_aplicado' => $request->recargo_aplicado ?? 0,
            'precio_reserva' => $total,
            'observaciones' => $request->observaciones,
        ]);
    
        $detalle = DetalleReservaHabitacion::create($request->only([
            'id_habitacion',
            'fecha_inicio',
            'fecha_fin',
            'cantidad_personas',
            'noches',
            'precio_noche',
            'descuento_aplicado',
            'recargo_aplicado',
            'precio_reserva',
            'observaciones',
        ]));

        ReservaHabitacion::create([
            'id_cliente' => $request->id_cliente,
            'id_detalle_reserva_hab' => $detalle->id_detalle_reserva_hab,
        ]);

        return redirect()->route('reservash.gestion.index')->with('success', 'Reserva creada correctamente.');
    }

    public function destroy(ReservaHabitacion $reserva)
    {
        $reserva->delete();
        return redirect()->route('reservash.gestion.index')->with('success', 'Reserva eliminada.');
    }

    public function papelera()
    {
        $reservas = ReservaHabitacion::onlyTrashed()->with(['cliente', 'detalle'])->get();
        return view('administrador.reservash.papelera', compact('reservas'));
    }

    public function restaurar($id)
    {
        $reserva = ReservaHabitacion::withTrashed()->findOrFail($id);
        $reserva->restore();
        return redirect()->route('reservash.papelera')->with('success', 'Reserva restaurada.');
    }
}