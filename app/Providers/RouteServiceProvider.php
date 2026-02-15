<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class RouteServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap services.
     */
    public function boot(): void
    {    
        $filename = 'web.php';
        $routeHotel = 'routes/hotel/';
        $routeCliente = 'routes/cliente/';
        $routeBackoffice = 'routes/backoffice/';
        $this->loadRoutesFrom(base_path($routeHotel. $filename));
        $this->loadRoutesFrom(base_path($routeBackoffice.'finance/'. $filename));
        $this->loadRoutesFrom(base_path($routeBackoffice.'includes/'. $filename));
        $this->loadRoutesFrom(base_path($routeBackoffice.'restaurant/'. $filename));
        $this->loadRoutesFrom(base_path($routeBackoffice.'rooms/'. $filename));
        $this->loadRoutesFrom(base_path($routeBackoffice.'users/'. $filename));
        $this->loadRoutesFrom(base_path($routeCliente. $filename));
    }
}