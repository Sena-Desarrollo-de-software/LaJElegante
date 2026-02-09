<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        $this->loadMigrationsFrom([
            database_path('migrations/laravel_basic'),
            database_path('migrations/finance'),
            database_path('migrations/restaurant'),
            database_path('migrations/rooms'),
            database_path('migrations/users'),
    ]);
    }
}
