<?php
use App\Http\Controllers\Modules\Finance\TarifaController;
use App\Http\Controllers\Modules\Finance\TemporadaController;
use Illuminate\Support\Facades\Route;
/*
|--------------------------------------------------------------------------
| TARIFAS
|--------------------------------------------------------------------------
*/
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
Route::prefix('temporadas')->name('temporadas.')->group(function () {
    Route::get('papelera', [TemporadaController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TemporadaController::class, 'restaurar'])->name('restaurar');
    Route::resource('gestion', TemporadaController::class)->parameters(['gestion' => 'temporada']);
});