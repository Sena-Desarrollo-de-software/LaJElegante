<?php

namespace App\Exports;

use App\Models\Cliente;
use Illuminate\Database\Eloquent\Builder;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;

class ClientesExport implements FromCollection, WithHeadings, WithMapping
{
    protected $filtros;

    public function __construct($filtros = [])
    {
        $this->filtros = $filtros;
    }

    /**
     * Devuelve la query base filtrada
     */
    public function query(): Builder
    {
        $query = Cliente::with('tipoCliente'); 

        if(!empty($this->filtros['estado'])) {
            $query->where('estado', $this->filtros['estado']);
        }

        if(!empty($this->filtros['tipo'])) {
            $query->where('id_tipo_cliente', $this->filtros['tipo']);
        }

        if(!empty($this->filtros['desde']) && !empty($this->filtros['hasta'])) {
            $query->whereBetween('created_at', [$this->filtros['desde'], $this->filtros['hasta']]);
        }

        return $query;
    }

    /**
     * Usado por Excel
     */
    public function collection()
    {
        return $this->query()->get();
    }

    public function map($cliente): array
    {
        return [
            $cliente->id_cliente,
            $cliente->nombre,
            $cliente->apellido,
            $cliente->email_info,
            $cliente->tipoCliente->nombre_tipo ?? 'Sin tipo', 
            $cliente->saludo,
            $cliente->prefijo_telefono,
            $cliente->numero_telefono,
            ucfirst($cliente->estado),
            $cliente->created_at ? $cliente->created_at->format('d/m/Y H:i') : '',
            $cliente->updated_at ? $cliente->updated_at->format('d/m/Y H:i') : '',
        ];
    }

    public function headings(): array
    {
        return [
            'ID',
            'Nombre',
            'Apellido',
            'Email',
            'Tipo Cliente',
            'Saludo',
            'Prefijo Teléfono',
            'Número Teléfono',
            'Estado',
            'Creado',
            'Actualizado'
        ];
    }
}