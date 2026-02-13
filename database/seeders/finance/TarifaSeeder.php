<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use App\Models\Tarifa;

class TarifaSeeder extends Seeder
{
    public function run(): void
    {
        Tarifa::create([
            'id_tipo_habitacion' => 1, 
            'id_temporada' => 3,
            'tarifa_fija' => 70000,
        ]);

        Tarifa::create([
            'id_tipo_habitacion' => 2, 
            'id_temporada' => 3,
            'tarifa_fija' => 120000,
        ]);

        Tarifa::create([
            'id_tipo_habitacion' => 3,
            'id_temporada' => 3,
            'tarifa_fija' => 180000,
        ]);

        Tarifa::create([
            'id_tipo_habitacion' => 4,
            'id_temporada' => 3,
            'tarifa_fija' => 210000,
        ]);
    }
}