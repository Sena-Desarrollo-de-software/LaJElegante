<?php
use App\Http\Controllers\Backoffice\Includes\DashboardController;
/*
|--------------------------------------------------------------------------
| DASHBOARD
|--------------------------------------------------------------------------
*/
Route::prefix('dashboard')->name('dashboard.')->group(function () {
    Route::get('dashboard', [DashboardController::class, 'index'])
        ->name('dashboard');
});