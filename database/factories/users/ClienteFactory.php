<?php

namespace Database\Factories;

use App\Models\Cliente;
use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;

class ClienteFactory extends Factory
{
    protected $model = Cliente::class;

    public function definition(): array
    {
        return [
            'id_tipo_cliente' => $this->faker->randomElement([1, 2]), // 1 = Huésped, 2 = No registrado
            'nombre' => $this->faker->firstName,
            'apellido' => $this->faker->lastName,
            'email_info' => $this->faker->unique()->safeEmail,
            'contrasena' => Hash::make('password123'), // contraseña estándar para pruebas
            'saludo' => $this->faker->randomElement(['MR','MS','MX']),
            'numero_telefono' => $this->faker->numerify('3#########'), // número colombiano
            'prefijo_telefono' => '+57',
            'estado' => $this->faker->randomElement(['activo', 'inactivo']),
        ];
    }

    /**
     * Estado específico: Huésped
     */
    public function huesped(): static
    {
        return $this->state(fn (array $attributes) => [
            'id_tipo_cliente' => 1,
        ]);
    }

    /**
     * Estado específico: No registrado
     */
    public function noRegistrado(): static
    {
        return $this->state(fn (array $attributes) => [
            'id_tipo_cliente' => 2,
        ]);
    }
}