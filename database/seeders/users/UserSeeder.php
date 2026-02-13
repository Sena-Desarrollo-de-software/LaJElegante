<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        $roles = [
            'recepcionista' => ['name' => 'Recepcionista', 'email' => 'recepcionista@lje.com'],
            'asistente_administrativo' => ['name' => 'Asistente Administrativo', 'email' => 'asistente@lje.com'],
            'gerente_alimentos' => ['name' => 'Gerente de Alimentos', 'email' => 'gerente_alimentos@lje.com'],
            'gerente_habitaciones' => ['name' => 'Gerente de Habitaciones', 'email' => 'gerente_habitaciones@lje.com'],
            'gerente_general' => ['name' => 'Gerente General', 'email' => 'gerente_general@lje.com'],
            'administrador' => ['name' => 'Administrador', 'email' => 'admin@lje.com'],
        ];

        foreach ($roles as $role => $data) {
            User::updateOrCreate(
                ['email' => $data['email']],
                [
                    'name' => $data['name'],
                    'password' => Hash::make('password123'),
                    'role' => $role,
                ]
            );
        }
    }
}