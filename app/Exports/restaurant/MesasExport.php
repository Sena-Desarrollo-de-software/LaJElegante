<?php

namespace App\Exports\Restaurant;

use App\Models\Mesa;
use Maatwebsite\Excel\Concerns\FromCollection;

class MesasExport implements FromCollection
{
    public function collection()
    {
        return Mesa::all();
    }
}
