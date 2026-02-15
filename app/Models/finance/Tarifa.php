<?php

namespace App\Models\Finance;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Tarifa extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'tarifas';
    protected $primaryKey = 'id_tarifa';

    protected $fillable = [
        'tarifa_fija',
        'precio_final',
        'estado',
        'id_temporada',
    ];

    // Relación con Temporada
    public function temporada()
    {
        return $this->belongsTo(Temporada::class, 'id_temporada', 'id_temporada');
    }
}