<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Mesa extends Model
{
    use HasFactory;

    protected $table = 'mesas';
    protected $primaryKey = 'id_mesa';

    protected $fillable = [
        'numero_mesa',
        'capacidad',
        'ubicacion',
        'activo', // agregar para ocultar/mostrar
    ];

    protected $casts = [
        'activo' => 'boolean', // para interpretar como booleano
    ];

    // Relación: una mesa puede tener muchas reservas
    public function reservas()
    {
        return $this->hasMany(ReservaRestaurante::class, 'id_mesa', 'id_mesa');
    }
}
