<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class TipoCliente extends Model
{
    use HasFactory, SoftDeletes;

    protected $table = 'tipo_cliente';
    protected $primaryKey = 'id_tipo_cliente';
    protected $keyType = 'int';

    protected $fillable = [
        'nombre_tipo',
    ];

    protected $dates = ['deleted_at'];

    public function clientes()
    {
        return $this->hasMany(Cliente::class, 'id_tipo_cliente', 'id_tipo_cliente');
    }
}