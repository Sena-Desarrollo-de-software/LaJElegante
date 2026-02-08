<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Route;

class EmpleadoAuthController extends Controller
{
    public function showLoginForm()
    {
        return view('hotel.loginEmpleado');
    }

    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email'    => 'required|email',
            'password' => 'required|string',
        ]);

        $empleado = User::where('email', $credentials['email'])->first();

        if ($empleado && Hash::check($credentials['password'], $empleado->password)) {
            Auth::login($empleado);
            $request->session()->regenerate();

            $roleMap = [
                'administrador' => 'administrador',
                'recepcionista' => 'recepcionista',
                'asistente_administrativo' => 'asistente_administrativo',
                'gerente_alimentos' => 'gerente_alimentos',
                'gerente_habitaciones' => 'gerente_habitaciones',
                'gerente_general' => 'gerente_general',
            ];

            $roleKey = $roleMap[$empleado->role] ?? null;

            if ($roleKey && Route::has("{$roleKey}.dashboard")) {
                return redirect()->route("{$roleKey}.dashboard");
            } else {
                Auth::logout();
                return back()->withErrors([
                    'email' => "Rol '{$empleado->role}' no tiene dashboard asignado"
                ]);
            }
        }

        return back()->withErrors([
            'email' => 'Credenciales incorrectas'
        ])->onlyInput('email');
    }

    // Logout de empleados
    public function logout(Request $request)
{
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();

    // Agregar mensaje de éxito
    return redirect()->route('hotel.empleados.login.index')
                     ->with('success', 'Sesión cerrada correctamente.');
}

}