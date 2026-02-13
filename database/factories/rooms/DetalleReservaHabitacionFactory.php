<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use App\Models\DetalleReservaHabitacion;
use App\Models\Habitacion;
use Carbon\Carbon;

class DetalleReservaHabitacionFactory extends Factory
{
    protected $model = DetalleReservaHabitacion::class;

    public function definition(): array
    {
        $fecha_inicio = $this->faker->dateTimeBetween('now', '+1 year');
        $noches = $this->faker->numberBetween(1, 14); // máximo 2 semanas
        $fecha_fin = (clone $fecha_inicio)->modify("+{$noches} days");

        $precio_noche = $this->faker->randomFloat(2, 100, 500);

        return [
            'id_habitacion' => Habitacion::inRandomOrder()->first()->id_habitacion ?? 1,
            'fecha_inicio' => $fecha_inicio->format('Y-m-d'),
            'fecha_fin' => $fecha_fin->format('Y-m-d'),
            'cantidad_personas' => $this->faker->numberBetween(1, 4),
            'noches' => $noches,
            'precio_noche' => $precio_noche,
            'descuento_aplicado' => 0,
            'recargo_aplicado' => 0,
            'precio_reserva' => $precio_noche * $noches,
            'observaciones' => $this->faker->optional()->sentence(),
        ];
    }
}