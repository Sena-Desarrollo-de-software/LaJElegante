<?php

namespace App\Http\Controllers;

use App\Models\Cliente;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function showSignupForm()
    {
        return view('hotel.signup');
    }

    public function store(Request $request)
    {
        $request->validate([
            'nombre'           => 'required|string|max:255',
            'apellido'         => 'required|string|max:255',
            'email_info'       => 'required|email|unique:clientes,email_info',
            'password'         => 'required|string|min:8|confirmed',
            'saludo'           => 'required|in:MR,MS,MX',
            'numero_telefono'  => 'required|string|max:20',
            'prefijo_telefono' => 'required|string|max:5',
            'estado'           => 'in:activo,inactivo',
        ]);

        // Siempre será Huesped todos los registrados
        $huespedId = 1; 

        Cliente::create([
            'id_tipo_cliente'  => $huespedId,
            'email_info'       => $request->email_info,
            'contrasena'       => Hash::make($request->password),
            'nombre'           => $request->nombre,
            'apellido'         => $request->apellido,
            'saludo'           => $request->saludo,
            'numero_telefono'  => $request->numero_telefono,
            'prefijo_telefono' => $request->prefijo_telefono,
            'estado'           => $request->estado ?? 'activo',
        ]);

        return redirect()->route('hotel.login.index')
                         ->with('success', 'Cuenta creada con éxito. Ahora puedes iniciar sesión.');
    }

    public function showLoginForm()
    {
        return view('hotel.login');
    }

    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);
        
        $cliente = Cliente::where('email_info', $credentials['email'])->first();

        if ($cliente && Hash::check($credentials['password'], $cliente->contrasena)) {
            Auth::login($cliente); 
            $request->session()->regenerate();
            return redirect()->intended('/dashboard'); 
        }

        return back()->withErrors([
            'email' => 'Credenciales incorrectas',
        ])->onlyInput('email');
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect()->route('hotel.login.index');
    }
}