<?php

namespace App\Exports;

use App\Models\Tarifa;
use Maatwebsite\Excel\Concerns\FromCollection;

class TarifasExport implements FromCollection
{
    /**
    * @return \Illuminate\Support\Collection
    */
    public function collection()
    {
        return Tarifa::all();
    }
}
