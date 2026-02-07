<?php

namespace App\Exports;

use App\Models\User;
use Illuminate\Database\Eloquent\Builder;
use Maatwebsite\Excel\Concerns\FromCollection;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;

class UsersExport implements FromCollection, WithHeadings, WithMapping
{
    protected $filtros;

    public function __construct($filtros = [])
    {
        $this->filtros = $filtros;
    }

    public function query(): Builder
    {
        $query = User::query();

        if (!empty($this->filtros['role'])) {
            $query->where('role', $this->filtros['role']);
        }

        if (!empty($this->filtros['desde']) && !empty($this->filtros['hasta'])) {
            $query->whereBetween('created_at', [$this->filtros['desde'], $this->filtros['hasta']]);
        }

        return $query;
    }

    /*Usado por Excel*/
    public function collection()
    {
        return $this->query()->get();
    }

    public function map($usuario): array
    {
        return [
            $usuario->id,
            $usuario->name,
            $usuario->email,
            ucfirst(str_replace('_',' ', $usuario->role)),
            $usuario->created_at ? $usuario->created_at->format('d/m/Y H:i') : '',
            $usuario->updated_at ? $usuario->updated_at->format('d/m/Y H:i') : '',
        ];
    }

    public function headings(): array
    {
        return [
            'ID',
            'Nombre',
            'Email',
            'Rol',
            'Creado',
            'Actualizado',
        ];
    }
}