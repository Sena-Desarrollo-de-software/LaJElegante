<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class TipoHabitacion extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'tipo_habitacion';
    protected $primaryKey = 'id_tipo_habitacion';

    protected $fillable = [
        'nombre_tipo',
        'descripcion',
        'capacidad_maxima',
    ];

    protected $dates = ['deleted_at'];
}