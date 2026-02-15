<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\DB;

class MesaSeeder extends Seeder
{
    public function run(): void
    {
        DB::table('mesas')->insert([
            ['numero_mesa' => 1, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral superior derecho'],
            ['numero_mesa' => 2, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral superior centro'],
            ['numero_mesa' => 3, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral superior izquierdo'],
            ['numero_mesa' => 4, 'capacidad' => 2, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'centro izquierdo'],
            ['numero_mesa' => 5, 'capacidad' => 2, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'centro'],
            ['numero_mesa' => 6, 'capacidad' => 2, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'centro derecho'],
            ['numero_mesa' => 7, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral inferior derecho'],
            ['numero_mesa' => 8, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral inferior centro'],
            ['numero_mesa' => 9, 'capacidad' => 4, 'zona' => 'Restaurante', 'ubicacion_detalle' => 'lateral inferior izquierdo'],
            ['numero_mesa' => 10, 'capacidad' => 6, 'zona' => 'Terraza', 'ubicacion_detalle' => 'inferior'],
            ['numero_mesa' => 11, 'capacidad' => 6, 'zona' => 'Terraza', 'ubicacion_detalle' => 'superior'],
        ]);
    }
}