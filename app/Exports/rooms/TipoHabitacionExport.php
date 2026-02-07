<?php

namespace App\Exports;

use App\Models\TipoHabitacion;
use Maatwebsite\Excel\Concerns\FromCollection;

class TipoHabitacionExport implements FromCollection
{
    /**
    * @return \Illuminate\Support\Collection
    */
    public function collection()
    {
        return TipoHabitacion::all();
    }
}
