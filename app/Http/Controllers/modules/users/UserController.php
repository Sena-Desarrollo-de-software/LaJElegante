<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function index()
    {
        $usuarios = User::all();
        return view('administrador.users.index', compact('usuarios'));
    }

    public function create()
    {
        return view('administrador.users.create');
    }

    public function store(Request $request)
    {
        $request->validate([
            'name'     => 'required|string|max:255',
            'email'    => 'required|email|unique:users,email',
            'password' => 'required|string|min:8|confirmed',
            'role'     => 'required|in:recepcionista,asistente_administrativo,gerente_alimentos,gerente_habitaciones,gerente_general,administrador',
        ]);

        User::create([
            'name'     => $request->name,
            'email'    => $request->email,
            'password' => Hash::make($request->password),
            'role'     => $request->role,
        ]);

        return redirect()->route('users.gestion.index')->with('success', 'Usuario creado correctamente.');
    }

    public function edit($id)
    {
        $usuario = User::findOrFail($id);
        return view('administrador.users.edit', compact('usuario'));
    }

    public function update(Request $request, $id)
    {
        $usuario = User::findOrFail($id);

        $request->validate([
            'name'  => 'required|string|max:255',
            'email' => 'required|email|unique:users,email,' . $usuario->id,
            'role'  => 'required|in:recepcionista,asistente_administrativo,gerente_alimentos,gerente_habitaciones,gerente_general,administrador',
        ]);

        $usuario->update([
            'name'  => $request->name,
            'email' => $request->email,
            'role'  => $request->role,
        ]);

        if ($request->filled('password')) {
            $usuario->update([
                'password' => Hash::make($request->password),
            ]);
        }

        return redirect()->route('users.gestion.index')->with('success', 'Usuario actualizado correctamente.');
    }

    public function destroy($id)
    {
        $usuario = User::findOrFail($id);
        $usuario->delete();

        return redirect()->route('users.gestion.index')
                         ->with('success', 'Usuario eliminado con éxito.');
    }

    public function papelera()
    {
        $usuarios = User::onlyTrashed()->get();
        return view('administrador.users.papelera', compact('usuarios'));
    }

    public function restaurar($id)
    {
        $usuario = User::onlyTrashed()->where('id', $id)->firstOrFail();
        $usuario->restore();

        return redirect()->route('users.papelera')
                         ->with('success', 'Usuario restaurado correctamente.');
    }
}