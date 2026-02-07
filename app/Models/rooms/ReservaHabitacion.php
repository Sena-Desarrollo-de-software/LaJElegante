<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class ReservaHabitacion extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'reserva_habitacion';
    protected $primaryKey = 'id_reserva_habitacion';

    protected $fillable = [
        'id_cliente',
        'id_detalle_reserva_hab',
    ];

    public function cliente()
    {
        return $this->belongsTo(Cliente::class, 'id_cliente', 'id_cliente');
    }

    public function detalle()
    {
        return $this->hasOne(DetalleReservaHabitacion::class, 'id_detalle_reserva_hab', 'id_detalle_reserva_hab');
    }
}