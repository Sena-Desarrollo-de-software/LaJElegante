<?php
use App\Http\Controllers\Modules\Users\ClienteController;
use App\Http\Controllers\TipoClienteController;
use App\Http\Controllers\UserController;
use App\Http\Controllers\ReporteClienteController;
use App\Http\Controllers\ReporteUserController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| CLIENTES
|--------------------------------------------------------------------------
*/
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
| TIPO CLIENTE
|--------------------------------------------------------------------------
*/
Route::prefix('tipo_cliente')->name('tipo_cliente.')->group(function () {
    Route::resource('gestion', TipoClienteController::class)->parameters(['gestion' => 'tipo_cliente']);
    Route::get('papelera', [TipoClienteController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [TipoClienteController::class, 'restaurar'])->name('restaurar');
});

/*
|--------------------------------------------------------------------------
| USERS
|--------------------------------------------------------------------------
*/
Route::prefix('users')->name('users.')->group(function () {
    Route::resource('gestion', UserController::class)->parameters(['gestion' => 'user']);
    Route::get('papelera', [UserController::class, 'papelera'])->name('papelera');
    Route::patch('restaurar/{id}', [UserController::class, 'restaurar'])->name('restaurar');

    // Reportes
    Route::get('reportes', [ReporteUserController::class, 'index'])->name('reportes');
    Route::get('exportar-excel', [ReporteUserController::class, 'exportarExcel'])->name('exportar.excel');
    Route::get('exportar-pdf', [ReporteUserController::class, 'exportarPDF'])->name('exportar.pdf');
});