<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use App\Models\Temporada;

class TemporadaSeeder extends Seeder
{
    public function run(): void
    {
        Temporada::create([
            'nombre' => 'alta',
            'fecha_inicio' => '2025-12-15',
            'fecha_fin' => '2026-01-15',
            'modificador_precio' => '1.45',
        ]);

        Temporada::create([
            'nombre' => 'media',
            'fecha_inicio' => '2025-06-15',
            'fecha_fin' => '2025-07-15',
            'modificador_precio' => '1.25',
        ]);

        Temporada::create([
            'nombre' => 'baja',
            'fecha_inicio' => '2025-02-01',
            'fecha_fin' => '2025-03-15',
            'modificador_precio' => '0.90',
        ]);
    }
}
