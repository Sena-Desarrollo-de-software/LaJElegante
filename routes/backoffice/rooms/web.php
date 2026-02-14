<?php
use App\Http\Controllers\Modules\Rooms\ReservaHabitacionController;
use App\Http\Controllers\Modules\Rooms\TipoHabitacionController;
use App\Http\Controllers\Modules\Rooms\HabitacionController;
use App\Exports\Rooms\ReservaHabitacionExport;
use App\Exports\Rooms\HabitacionesExport;
use Illuminate\Support\Facades\Route;
/*
|--------------------------------------------------------------------------
| HABITACIONES
|--------------------------------------------------------------------------
*/
// Habitaciones
Route::prefix('habitaciones')->name('habitaciones.')->group(function () {
    Route::get('papelera', [HabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [HabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion',HabitacionController::class)->parameters(['gestion' => 'habitacion']);

    Route::get('reportes', [HabitacionesExport::class, 'index'])->name('reportes');
    Route::get('exportar/excel', [HabitacionesExport::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar/pdf', [HabitacionesExport::class, 'exportarPDF'])->name('exportar.pdf');

    Route::get('{id}/capacidad', [HabitacionController::class, 'capacidadMaxima'])->name('capacidad');
    Route::get('{id}/tarifa', [ReservaHabitacionController::class, 'getTarifa'])->name('tarifa');
});
/*
|--------------------------------------------------------------------------
| TIPO HABITACIÓN
|--------------------------------------------------------------------------
*/
Route::prefix('tipo_habitacion')->name('tipo_habitacion.')->group(function () {
    Route::get('papelera', [TipoHabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TipoHabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', TipoHabitacionController::class)->parameters(['gestion' => 'tipo_habitacion']);
});

/*
|--------------------------------------------------------------------------
| RESERVAS DE HABITACIÓN
|--------------------------------------------------------------------------
*/
Route::prefix('reservash')->name('reservash.')->group(function () {
    Route::get('papelera', [ReservaHabitacionController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [ReservaHabitacionController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', ReservaHabitacionController::class)->parameters(['gestion' => 'reserva']);
    Route::get('reportes', [ReservaHabitacionExport::class, 'index'])->name('reportes');
    Route::get('exportar-excel', [ReservaHabitacionExport::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar-pdf', [ReservaHabitacionExport::class, 'exportarPDF'])->name('exportar.pdf');
});