<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use App\Models\TipoCliente;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;



class ClienteController extends Controller
{
    public function index()
    {
        $clientes = Cliente::with('tipoCliente')->get();
        return view('administrador.clientes.index', compact('clientes'));
    }

    public function create()
{
    $tipos = TipoCliente::all();
    return view('administrador.clientes.create', compact('tipos'));
}

    public function store(Request $request)
    {
        $request->validate([
            'nombre' => 'required|string|max:255',
            'apellido' => 'required|string|max:255',
            'email_info' => 'required|email|unique:clientes,email_info',
            'contrasena' => 'required|string|min:8|confirmed',
            'id_tipo_cliente' => 'required|exists:tipo_cliente,id_tipo_cliente',
            'numero_telefono' => 'nullable|string|max:20',
            'prefijo_telefono' => 'required|string|max:5',
            'estado' => 'required|string',
        ]);

            Cliente::create([
        'nombre'          => $request->nombre,
        'apellido'        => $request->apellido,
        'email_info'      => $request->email_info,
        'contrasena'      => Hash::make($request->contrasena),
        'id_tipo_cliente' => $request->id_tipo_cliente,
        'numero_telefono' => $request->numero_telefono,
        'prefijo_telefono' => $request->prefijo_telefono,
        'estado'          => $request->estado,
    ]);

        return redirect()->route('clientes.gestion.index')
                        ->with('success', 'Cliente creado correctamente.');
    }


    public function show(Cliente $cliente)
    {
        return view('administrador.clientes.index', compact('cliente'));
    }

    public function edit(Cliente $cliente)
    {
        $tipos = TipoCliente::all();
        return view('administrador.clientes.edit', compact('cliente', 'tipos'));
    }

public function update(Request $request, Cliente $cliente)
{
    $request->validate([
        'id_tipo_cliente' => 'required|exists:tipo_cliente,id_tipo_cliente',
        'email_info' => 'required|email|unique:clientes,email_info,' . $cliente->id_cliente . ',id_cliente',
        'contrasena' => 'nullable|string|min:8|confirmed',
        'nombre' => 'required|string|max:255',
        'apellido' => 'required|string|max:255',
        'numero_telefono' => 'nullable|string|max:20',
        'prefijo_telefono' => 'required|string|max:5',
        'estado' => 'required|in:activo,inactivo',
    ]);

    $data = $request->all();

    if (!empty($request->contrasena)) {
        $data['contrasena'] = Hash::make($request->contrasena);
    } else {
        unset($data['contrasena']);
    }

    $cliente->update($data);

    return redirect()->route('clientes.gestion.index')
                     ->with('success', 'Cliente actualizado con éxito.');
}

    public function destroy(Cliente $cliente)
    {
         $cliente->delete();
        return redirect()->route('clientes.gestion.index')
            ->with('success', 'Cliente eliminado con éxito');
    }
        public function papelera()
    {
        $clientes = Cliente::onlyTrashed()->get();
        return view('administrador.clientes.papelera', compact('clientes'));
    }

    public function restaurar($id)
    {
        $cliente = Cliente::onlyTrashed()->where('id_cliente', $id)->firstOrFail();
        $cliente->restore();

        return redirect()->route('clientes.papelera')->with('success', 'Cliente restaurado correctamente');
    }
}