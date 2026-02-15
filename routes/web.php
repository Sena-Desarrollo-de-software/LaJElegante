<?php
/*
// Controladores de administración
use App\Http\Controllers\ClienteController;
use App\Http\Controllers\ReservaHabitacionController;
use App\Http\Controllers\TarifaController;
use App\Http\Controllers\TemporadaController;
use App\Http\Controllers\TipoClienteController;
use App\Http\Controllers\TipoHabitacionController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\HabitacionController;
use App\Http\Controllers\MesaController;
use App\Http\Controllers\ReservaRestauranteController;

// Controladores de reportes
use App\Http\Controllers\ReporteClienteController;
use App\Http\Controllers\ReporteUserController;
use App\Http\Controllers\ReporteHabitacionController;
use App\Http\Controllers\ReporteReservaHabitacionController;

// Controladores de autenticación
use App\Http\Controllers\AuthController;
use App\Http\Controllers\EmpleadoAuthController;

// Facades y utilidades
use Illuminate\Support\Facades\Route;
use Maatwebsite\Excel\Facades\Excel;
use Barryvdh\DomPDF\Facade\Pdf;

// Exports
use App\Exports\ReservasRestauranteExport;
use App\Exports\MesasExport;



// Modelos
use App\Models\ReservaRestaurante;

/*
|--------------------------------------------------------------------------
| CLIENTES
|--------------------------------------------------------------------------
*/
/*
Route::prefix('clientes')->name('clientes.')->group(function () {
    // CRUD
    Route::get('papelera', [ClienteController::class, 'papelera'])->name('papelera');
    Route::patch('{id}/restaurar', [ClienteController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', ClienteController::class)->parameters(['gestion' => 'cliente']);

    // Reportes
    Route::get('reportes', [ReporteClienteController::class, 'index'])->name('reportes');
    Route::get('exportar-excel', [ReporteClienteController::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar-pdf', [ReporteClienteController::class, 'exportarPDF'])->name('exportar.pdf');
});

/*
|--------------------------------------------------------------------------
| HABITACIONES
|--------------------------------------------------------------------------
*/
/*
// Habitaciones
Route::prefix('habitaciones')->name('habitaciones.')->group(function () {
    Route::get('papelera', [HabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [HabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion',HabitacionController::class)->parameters(['gestion' => 'habitacion']);

    Route::get('reportes', [ReporteHabitacionController::class, 'index'])->name('reportes');
    Route::get('exportar/excel', [ReporteHabitacionController::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar/pdf', [ReporteHabitacionController::class, 'exportarPDF'])->name('exportar.pdf');

    Route::get('{id}/capacidad', [App\Http\Controllers\HabitacionController::class, 'capacidadMaxima'])->name('capacidad');
    Route::get('{id}/tarifa', [App\Http\Controllers\ReservaHabitacionController::class, 'getTarifa'])->name('tarifa');
});

/*
|--------------------------------------------------------------------------
| RESERVAS DE HABITACIÓN
|--------------------------------------------------------------------------
*/
/*
Route::prefix('reservash')->name('reservash.')->group(function () {
    Route::get('papelera', [ReservaHabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [ReservaHabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', ReservaHabitacionController::class)->parameters(['gestion' => 'reserva']);
    Route::get('reportes', [ReporteReservaHabitacionController::class, 'index'])->name('reportes');
    Route::get('exportar-excel', [ReporteReservaHabitacionController::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar-pdf', [ReporteReservaHabitacionController::class, 'exportarPDF'])->name('exportar.pdf');
});

/*
|--------------------------------------------------------------------------
| TARIFAS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('tarifas')->name('tarifas.')->group(function () {
    Route::get('papelera', [TarifaController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TarifaController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', TarifaController::class)->parameters(['gestion' => 'tarifa']);
    Route::get('{habitacion}/por-habitacion', [TarifaController::class, 'getTarifaPorHabitacion'])->name('porHabitacion');
});

/*
|--------------------------------------------------------------------------
| TEMPORADAS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('temporadas')->name('temporadas.')->group(function () {
    Route::get('papelera', [TemporadaController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TemporadaController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', TemporadaController::class)->parameters(['gestion' => 'temporada']);
});

/*
|--------------------------------------------------------------------------
| TIPO CLIENTE
|--------------------------------------------------------------------------
*/
/*
Route::prefix('tipo_cliente')->name('tipo_cliente.')->group(function () {
    Route::resource('gestion', TipoClienteController::class)->parameters(['gestion' => 'tipo_cliente']);
    Route::get('papelera', [TipoClienteController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TipoClienteController::class, 'restaurar'])->name('restaurar');
});

/*
|--------------------------------------------------------------------------
| TIPO HABITACIÓN
|--------------------------------------------------------------------------
*/
/*
Route::prefix('tipo_habitacion')->name('tipo_habitacion.')->group(function () {
    Route::get('papelera', [TipoHabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TipoHabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', TipoHabitacionController::class)->parameters(['gestion' => 'tipo_habitacion']);
});


/*
|--------------------------------------------------------------------------
| MESAS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('mesas')->name('mesas.')->group(function () {
    // Ocultar y mostrar mesas
    Route::patch('{id}/ocultar', [MesaController::class, 'ocultar'])->name('ocultar');
    Route::patch('{id}/mostrar', [MesaController::class, 'mostrar'])->name('mostrar');

    // CRUD de mesas, excepto destroy
    Route::resource('gestion', MesaController::class)->except(['destroy']);

    // Reportes
    Route::get('export-excel', function () {
        return Excel::download(new MesasExport, 'mesas.xlsx');
    })->name('exportExcel');

    Route::get('export-pdf', function () {
        $mesas = \App\Models\Mesa::all();
        $pdf = Pdf::loadView('administrador.mesas.pdf', compact('mesas'));
        return $pdf->download('mesas.pdf');
    })->name('exportPDF');

    // Vistas y acciones extras si llegas a necesitarlas
    // Ejemplo: mesas disponibles para reservas
    Route::get('disponibles', [MesaController::class, 'mesasDisponibles'])->name('disponibles');
    Route::post('reservar', [MesaController::class, 'reservarMesa'])->name('reservar');
});


/*
|--------------------------------------------------------------------------
| RESERVAS RESTAURANTE
|--------------------------------------------------------------------------
*/
/*
Route::prefix('reservasr')->name('reservasr.')->group(function () {
    // CRUD de reservas
    Route::patch('{id}/ocultar', [ReservaRestauranteController::class, 'ocultar'])->name('ocultar');
    Route::patch('{id}/mostrar', [ReservaRestauranteController::class, 'mostrar'])->name('mostrar');
    Route::resource('gestion', ReservaRestauranteController::class)->except(['destroy']);

    // Reportes
    Route::get('export-excel', function () {
        return Excel::download(new ReservasRestauranteExport, 'reservas.xlsx');
    })->name('exportExcel');

    Route::get('export-pdf', function () {
        $reservas = ReservaRestaurante::all();
        $pdf = Pdf::loadView('administrador.reservasr.pdf', compact('reservas'));
        return $pdf->download('reservas.pdf');
    })->name('exportPDF');

    // Vistas y acciones extras
    Route::get('mesas', [ReservaRestauranteController::class, 'mesasDisponibles'])->name('mesas');
    Route::post('mesa', [ReservaRestauranteController::class, 'storeMesa'])->name('storeMesa');
});

/*
|--------------------------------------------------------------------------
| USERS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('users')->name('users.')->group(function () {
    Route::resource('gestion', UserController::class)->parameters(['gestion' => 'user']);
    Route::get('papelera', [UserController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [UserController::class, 'restaurar'])->name('restaurar');

    // Reportes
    Route::get('reportes', [ReporteUserController::class, 'index'])->name('reportes');
    Route::get('exportar-excel', [ReporteUserController::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar-pdf', [ReporteUserController::class, 'exportarPDF'])->name('exportar.pdf');
});

/*
|--------------------------------------------------------------------------
| INDEX VISTAS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('hotel')->name('hotel.')->group(function () {
    Route::get('/', function () {
        return view('hotel.lobby');
    })->name('lobby.index');

    Route::get('/restaurante', function () {
        return view('hotel.restaurante');
    })->name('restaurante.index');

    Route::get('/habitaciones', function () {
        return view('hotel.habitaciones');
    })->name('habitaciones.index');

    Route::get('/terminos', function () {
        return view('hotel.terminos');
    })->name('terminos.index');

    // Huespéd
    Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login.index');
    Route::post('/login', [AuthController::class, 'login'])->name('login.process');
    Route::get('/signup', [AuthController::class, 'showSignupForm'])->name('signup.index');
    Route::post('/signup', [AuthController::class, 'store'])->name('signup.process');
    
    // Empleados
    Route::get('/empleados/login', [EmpleadoAuthController::class, 'showLoginForm'])->name('empleados.login.index');
    Route::post('/empleados/login', [EmpleadoAuthController::class, 'login'])->name('empleados.login.process');
    Route::post('/empleados/logout', [EmpleadoAuthController::class, 'logout'])->name('empleados.logout');
});


/*
|--------------------------------------------------------------------------
| DASHBOARD
|--------------------------------------------------------------------------
*/
/*
Route::prefix('administrador')->name('administrador.')->group(function () {
    Route::get('dashboard', [\App\Http\Controllers\DashboardController::class, 'index'])
        ->name('dashboard');
});

/*
|--------------------------------------------------------------------------
| DASHBOARDS POR ROL DE EMPLEADOS
|--------------------------------------------------------------------------
*/
/*
Route::prefix('recepcionista')->name('recepcionista.')->group(function () {
    Route::get('dashboard', fn() => view('empleados.recepcionista.dashboard'))->name('dashboard');
});


Route::prefix('asistente_administrativo')->name('asistente_administrativo.')->group(function () {
    Route::get('dashboard', fn() => view('empleados.asistente_administrativo.dashboard'))->name('dashboard');
});


Route::prefix('gerente_alimentos')->name('gerente_alimentos.')->group(function () {
    Route::get('dashboard', fn() => view('empleados.gerente_alimentos.dashboard'))->name('dashboard');
});


Route::prefix('gerente_habitaciones')->name('gerente_habitaciones.')->group(function () {
    Route::get('dashboard', fn() => view('empleados.gerente_habitaciones.dashboard'))->name('dashboard');
});


Route::prefix('gerente_general')->name('gerente_general.')->group(function () {
    Route::get('dashboard', fn() => view('empleados.gerente_general.dashboard'))->name('dashboard');
});
*/