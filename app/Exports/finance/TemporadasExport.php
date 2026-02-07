<?php

namespace App\Exports;

use App\Models\Temporada;
use Maatwebsite\Excel\Concerns\FromCollection;

class TemporadasExport implements FromCollection
{
    /**
    * @return \Illuminate\Support\Collection
    */
    public function collection()
    {
        return Temporada::all();
    }
}
