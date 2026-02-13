<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $this->call([
            // Finance
            TarifaSeeder::class,
            TemporadaSeeder::class,
            // Restaurant
            MesaSeeder::class,
            ReservaRestauranteSeeder::class,
            // Rooms
            HabitacionSeeder::class,
            TipoHabitacionSeeder::class,
            ReservaHabitacionSeeder::class,
            // Users
            UserSeeder::class,
            ClienteSeeder::class,
            TipoClienteSeeder::class,
        ]);
    }
}