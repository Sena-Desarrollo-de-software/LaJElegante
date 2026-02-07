<?php

namespace App\Exports;

use App\Models\Mesa;
use Maatwebsite\Excel\Concerns\FromCollection;

class MesasExport implements FromCollection
{
    public function collection()
    {
        return Mesa::all();
    }
}
