<?php
namespace App\Http\Controllers;

use App\Models\Mesa;
use App\Models\ReservaRestaurante;
use Illuminate\Http\Request;

class MesaController extends Controller
{
    public function index(Request $request)
    {
        $mesas = $request->has('mostrar_ocultos') && $request->mostrar_ocultos
            ? Mesa::all()
            : Mesa::where('activo', true)->get();

        return view('administrador.mesas.index', compact('mesas'));
    }

    public function create()
    {
        return view('administrador.mesas.gestion.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'numero_mesa'       => 'required|integer',
            'capacidad'         => 'required|integer',
            'zona'              => 'required|string|max:100',
            'ubicacion_detalle' => 'nullable|string|max:255',
        ]);

        Mesa::create(array_merge($request->all(), ['activo' => true]));

        return redirect()->route('mesas.gestion.index')
            ->with('success', 'Mesa creada correctamente');
    }

    public function show($id)
    {
        $mesa = Mesa::findOrFail($id);
        return view('administrador.mesas.gestion.show', compact('mesa'));
    }

    public function edit($id)
    {
        $mesa = Mesa::findOrFail($id);
        return view('administrador.mesas.gestion.edit', compact('mesa'));
    }

    public function update(Request $request, $id)
    {
        $mesa = Mesa::findOrFail($id);

        $request->validate([
            'numero_mesa'       => 'sometimes|integer',
            'capacidad'         => 'sometimes|integer',
            'zona'              => 'sometimes|string|max:100',
            'ubicacion_detalle' => 'nullable|string|max:255',
        ]);

        $mesa->update($request->all());

        return redirect()->route('mesas.gestion.index')
            ->with('success', 'Mesa actualizada correctamente');
    }

    public function ocultar($id)
    {
        $mesa = Mesa::findOrFail($id);
        $mesa->activo = false;
        $mesa->save();

        return redirect()->route('mesas.gestion.index')
            ->with('success', 'Mesa desactivada correctamente');
    }

    public function mostrar($id)
    {
        $mesa = Mesa::findOrFail($id);
        $mesa->activo = true;
        $mesa->save();

        return redirect()->route('mesas.gestion.index')
            ->with('success', 'Mesa reactivada correctamente');
    }

    // ------------------------
    // RESERVA DE MESAS
    // ------------------------
    public function reservarMesa(Request $request)
    {
        $request->validate([
            'id_mesa' => 'required|exists:mesas,id_mesa',
            'fecha'   => 'required|date',
            'hora'    => 'required|date_format:H:i',
        ]);

        $mesa = Mesa::findOrFail($request->id_mesa);

        $existeReserva = ReservaRestaurante::where('id_mesa', $mesa->id_mesa)
            ->where('fecha_reserva', $request->fecha)
            ->where('hora_reserva', $request->hora)
            ->first();

        if ($existeReserva) {
            return redirect()->back()->with('error', 'Esta mesa ya está reservada para esa fecha y hora.');
        }

        ReservaRestaurante::create([
            'id_mesa'        => $mesa->id_mesa,
            'fecha_reserva'  => $request->fecha,
            'hora_reserva'   => $request->hora,
            'id_cliente'     => $request->id_cliente ?? null,
            'numero_personas'=> $mesa->capacidad,
            'estado_reserva' => 'pendiente',
            'activo'         => true,
        ]);

        return redirect()->back()->with('success', 'Mesa reservada correctamente.');
    }

    // ------------------------
    // MESAS DISPONIBLES (vista separada)
    // ------------------------
    public function mesasDisponibles()
    {
        $mesas = Mesa::all();
        return view('administrador.ReservasMesas.mesasDisponibles', compact('mesas'));
    }
}
