<?php
// Controladores de administración
use App\Http\Controllers\Modules\Restaurant\MesaController;
use App\Http\Controllers\Modules\Restaurant\ReservaRestauranteController;
use Illuminate\Support\Facades\Route;
use Maatwebsite\Excel\Facades\Excel;
use Barryvdh\DomPDF\Facade\Pdf;
use App\Exports\Restaurant\ReservasRestauranteExport;
use App\Exports\Restaurant\MesasExport;
use App\Models\Restaurant\ReservaRestaurante;
/*
|--------------------------------------------------------------------------
| MESAS
|--------------------------------------------------------------------------
*/
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