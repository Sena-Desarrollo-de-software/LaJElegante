<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\Habitacion;

class HabitacionSeeder extends Seeder
{
    public function run(): void
    {
        $habitaciones = [
            // Piso 1
            ['numero_habitacion' => 101, 'id_tipo_habitacion' => 3], // familiar
            ['numero_habitacion' => 102, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 103, 'id_tipo_habitacion' => 3], // familiar
            ['numero_habitacion' => 104, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 105, 'id_tipo_habitacion' => 3], // familiar
            ['numero_habitacion' => 106, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 107, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 108, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 109, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 110, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 111, 'id_tipo_habitacion' => 3], // familiar
            ['numero_habitacion' => 112, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 113, 'id_tipo_habitacion' => 3], // familiar
            ['numero_habitacion' => 114, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 115, 'id_tipo_habitacion' => 3], // familiar

            // Piso 2
            ['numero_habitacion' => 201, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 202, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 203, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 204, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 205, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 206, 'id_tipo_habitacion' => 4], // especial
            ['numero_habitacion' => 207, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 208, 'id_tipo_habitacion' => 4], // especial
            ['numero_habitacion' => 209, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 210, 'id_tipo_habitacion' => 4], // especial
            ['numero_habitacion' => 211, 'id_tipo_habitacion' => 1], // basica
            ['numero_habitacion' => 212, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 213, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 214, 'id_tipo_habitacion' => 2], // pareja
            ['numero_habitacion' => 215, 'id_tipo_habitacion' => 1], // basica
        ];

        foreach ($habitaciones as $habitacion) {
            Habitacion::create($habitacion);
        }
    }
}