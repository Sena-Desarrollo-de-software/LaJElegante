<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class ReservaRestaurante extends Model
{
    use HasFactory;

    protected $table = 'reservas_restaurante';
    protected $primaryKey = 'id_reserva';

    protected $fillable = [
        'id_cliente',
        'id_mesa',
        'fecha_reserva',
        'hora_reserva',
        'numero_personas',
        'estado_reserva',
        'activo', // nuevo campo
    ];

    protected $casts = [
        'activo' => 'boolean',
    ];

    // Relación: una reserva pertenece a un cliente
    public function cliente()
    {
        return $this->belongsTo(Cliente::class, 'id_cliente', 'id_cliente');
    }

    // Relación: una reserva pertenece a una mesa
    public function mesa()
    {
        return $this->belongsTo(Mesa::class, 'id_mesa', 'id_mesa');
    }
}
