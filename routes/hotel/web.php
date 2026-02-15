<?php

use App\Http\Controllers\Cliente\Auth\AuthController;
use App\Http\Controllers\Backoffice\Auth\EmpleadoAuthController;

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
        return view('hotel.tyc');
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