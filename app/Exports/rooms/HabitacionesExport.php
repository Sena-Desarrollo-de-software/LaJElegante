<?php

namespace App\Exports;

use App\Models\Habitacion;
use Maatwebsite\Excel\Concerns\FromQuery;
use Maatwebsite\Excel\Concerns\WithHeadings;

class HabitacionesExport implements FromQuery, WithHeadings
{
    protected $filters;

    public function __construct($filters = [])
    {
        $this->filters = $filters;
    }

    public function query()
    {
        $query = Habitacion::query()->with('tipoHabitacion');

        if (!empty($this->filters['estado_habitacion'])) {
            $query->where('estado_habitacion', $this->filters['estado_habitacion']);
        }

        if (!empty($this->filters['tipo'])) {
            $query->where('id_tipo_habitacion', $this->filters['tipo']);
        }

        if (!empty($this->filters['desde']) && !empty($this->filters['hasta'])) {
            $query->whereBetween('created_at', [$this->filters['desde'], $this->filters['hasta']]);
        }

        return $query;
    }

    public function headings(): array
    {
        return [
            'ID',
            'Número',
            'Estado',
            'Tipo de Habitación',
            'Creado en',
        ];
    }
}