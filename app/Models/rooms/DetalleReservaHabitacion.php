<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class DetalleReservaHabitacion extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'detalles_reserva_habitacion';
    protected $primaryKey = 'id_detalle_reserva_hab';

    protected $fillable = [
        'id_habitacion',
        'fecha_inicio',
        'fecha_fin',
        'cantidad_personas',
        'noches',
        'precio_noche',
        'descuento_aplicado',
        'recargo_aplicado',
        'precio_reserva',
        'observaciones',
    ];

    public function habitacion()
    {
        return $this->belongsTo(Habitacion::class, 'id_habitacion', 'id_habitacion');
    }

    public function reserva()
    {
        return $this->belongsTo(ReservaHabitacion::class, 'id_detalle_reserva_hab', 'id_detalle_reserva_hab');
    }
}