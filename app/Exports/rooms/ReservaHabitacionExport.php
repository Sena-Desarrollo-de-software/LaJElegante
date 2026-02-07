<?php

namespace App\Exports;

use App\Models\ReservaHabitacion;
use Illuminate\Database\Eloquent\Builder;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;

class ReservaHabitacionExport implements FromCollection, WithHeadings, WithMapping
{
    protected $filtros;

    public function __construct($filtros = [])
    {
        $this->filtros = $filtros;
    }

    public function query(): Builder
    {
        $query = ReservaHabitacion::with(['cliente', 'detalle.habitacion']);

        if (!empty($this->filtros['desde']) && !empty($this->filtros['hasta'])) {
            $query->whereBetween('created_at', [$this->filtros['desde'], $this->filtros['hasta']]);
        }

        return $query;
    }

    public function collection()
    {
        return $this->query()->get();
    }

    public function map($reserva): array
    {
        return [
            $reserva->id_reserva_habitacion,
            $reserva->cliente->nombre . ' ' . $reserva->cliente->apellido,
            $reserva->detalle->habitacion->numero_habitacion ?? 'N/A',
            $reserva->detalle->fecha_inicio,
            $reserva->detalle->fecha_fin,
            $reserva->detalle->cantidad_personas,
            $reserva->detalle->precio_reserva,
            $reserva->created_at->format('d/m/Y H:i'),
        ];
    }

    public function headings(): array
    {
        return [
            'ID',
            'Cliente',
            'Habitación',
            'Fecha Inicio',
            'Fecha Fin',
            'Personas',
            'Precio Total',
            'Creado',
        ];
    }
}