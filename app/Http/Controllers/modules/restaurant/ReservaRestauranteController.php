<?php

namespace App\Http\Controllers;

use App\Models\ReservaRestaurante;
use App\Models\Cliente;
use App\Models\Mesa;
use Illuminate\Http\Request;

class ReservaRestauranteController extends Controller
{
    // Listar reservas
    public function index(Request $request)
    {
        $query = ReservaRestaurante::with(['cliente', 'mesa']);

        if (!$request->has('mostrar_ocultos')) {
            $query->where('activo', true);
        }

        $reservas = $query->get();

        // Vista ajustada al prefijo administrador/reservasr/gestion
        return view('administrador.reservasr.index', compact('reservas'));
    }

    // Crear reserva (vista)
    public function create()
    {
        $clientes = Cliente::all();
        $mesas = Mesa::all();

        return view('administrador.reservasr.create', compact('clientes', 'mesas'));
    }

    // Guardar nueva reserva desde formulario tradicional
    public function store(Request $request)
    {
        $request->validate([
            'id_cliente' => 'required|exists:clientes,id_cliente',
            'id_mesa' => 'required|exists:mesas,id_mesa',
            'fecha_reserva' => 'required|date',
            'hora_reserva' => 'required',
            'numero_personas' => 'required|integer|min:1',
            'estado_reserva' => 'in:pendiente,confirmada,cancelada',
        ]);

        ReservaRestaurante::create(array_merge($request->all(), ['activo' => true]));

        return redirect()->route('reservasr.gestion.index')
            ->with('success', 'Reserva creada correctamente');
    }

    // Guardar reserva desde selección de mesa con cliente opcional
    public function storeMesa(Request $request)
    {
        $request->validate([
            'id_mesa' => 'required|exists:mesas,id_mesa',
            'fecha' => 'required|date',
            'hora' => 'required',
            'nombre_cliente' => 'nullable|string',
            'correo_cliente' => 'nullable|email',
        ]);

        $cliente_id = null;

        // Si se proporcionó nombre y correo, buscar cliente registrado
        if ($request->nombre_cliente && $request->correo_cliente) {
            $cliente = Cliente::where('nombre', $request->nombre_cliente)
                  ->where('email', $request->correo_cliente)
                  ->first();

            if ($cliente) {
                $cliente_id = $cliente->id_cliente;
            } else {
                return back()->with('error', 'No se encontró un cliente registrado con esos datos.');
            }
        }

        // Crear reserva
        ReservaRestaurante::create([
            'id_mesa' => $request->id_mesa,
            'id_cliente' => $cliente_id,
            'fecha_reserva' => $request->fecha,
            'hora_reserva' => $request->hora,
            'numero_personas' => $request->numero_personas ?? 1,
            'estado_reserva' => 'pendiente',
            'activo' => true,
        ]);

        return redirect()->route('reservasr.mesas')->with('success', 'Reserva creada correctamente.');
    }

    // Mostrar detalle de reserva
    public function show($id)
    {
        $reserva = ReservaRestaurante::with(['cliente', 'mesa'])->findOrFail($id);
        return view('administrador.reservasr.show', compact('reserva'));
    }

    // Editar reserva
    public function edit($id)
    {
        $reserva = ReservaRestaurante::findOrFail($id);
        $clientes = Cliente::all();
        $mesas = Mesa::all();

        return view('administrador.reservasr.edit', compact('reserva', 'clientes', 'mesas'));
    }

    // Actualizar reserva
    public function update(Request $request, $id)
    {
        $reserva = ReservaRestaurante::findOrFail($id);

        $request->validate([
            'id_cliente' => 'sometimes|exists:clientes,id_cliente',
            'id_mesa' => 'sometimes|exists:mesas,id_mesa',
            'fecha_reserva' => 'sometimes|date',
            'hora_reserva' => 'sometimes',
            'numero_personas' => 'sometimes|integer|min:1',
            'estado_reserva' => 'in:pendiente,confirmada,cancelada',
        ]);

        $reserva->update($request->all());

        return redirect()->route('reservasr.gestion.index')
            ->with('success', 'Reserva actualizada correctamente');
    }

    // Ocultar reserva (Eliminar temporal)
    public function ocultar($id)
    {
        $reserva = ReservaRestaurante::findOrFail($id);
        $reserva->activo = false;
        $reserva->save();

        return redirect()->route('reservasr.gestion.index')
            ->with('success', 'Reserva eliminada correctamente');
    }

    // Mostrar reserva (Restaurar)
    public function mostrar($id)
    {
        $reserva = ReservaRestaurante::findOrFail($id);
        $reserva->activo = true;
        $reserva->save();

        return redirect()->route('reservasr.gestion.index')
            ->with('success', 'Reserva restaurada correctamente');
    }

    // ------------------------
    // MESAS DISPONIBLES (vista separada)
    // ------------------------
    public function mesasDisponibles()
    {
        $mesas = Mesa::all();
        return view('administrador.reservasr.mesasDisponibles', compact('mesas'));
    }
}