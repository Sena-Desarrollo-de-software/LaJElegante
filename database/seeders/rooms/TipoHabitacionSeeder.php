<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use App\Models\TipoHabitacion;

class TipoHabitacionSeeder extends Seeder
{
    public function run(): void
    {
        TipoHabitacion::create([
            'nombre_tipo' => 'basica',
            'descripcion' => 'Habitación básica para 1 persona. [Completar descripción]',
            'capacidad_maxima' => 1
        ]);

        TipoHabitacion::create([
            'nombre_tipo' => 'pareja',
            'descripcion' => 'Habitación para 2 personas (máximo 3 con cama adicional). [Completar descripción]',
            'capacidad_maxima' => 2
        ]);

        TipoHabitacion::create([
            'nombre_tipo' => 'familiar',
            'descripcion' => 'Habitación para 5 personas (expandible a 6). [Completar descripción]',
            'capacidad_maxima' => 5
        ]);

        TipoHabitacion::create([
            'nombre_tipo' => 'especial',
            'descripcion' => 'Habitación especial y exclusiva. [Completar descripción]',
            'capacidad_maxima' => 2
        ]);
    }
}