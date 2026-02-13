<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Database\Console\Seeds\WithoutModelEvents;
use App\Models\TipoCliente;

class TipoClienteSeeder extends Seeder
{
    public function run(): void
    {
        TipoCliente::create(['nombre_tipo' => 'Huésped']);
        TipoCliente::create(['nombre_tipo' => 'No registrado']);
    }
}