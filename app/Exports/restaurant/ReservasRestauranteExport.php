<?php

namespace App\Exports;

use App\Models\ReservaRestaurante;
use Maatwebsite\Excel\Concerns\FromCollection;

class ReservasRestauranteExport implements FromCollection
{
    /**
    * @return \Illuminate\Support\Collection
    */
    public function collection()
    {
        return ReservaRestaurante::all();
    }
}
