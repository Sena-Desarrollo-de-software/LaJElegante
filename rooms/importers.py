from core.importers import BaseImporter

class HabitacionImporter(BaseImporter):
    from .forms import HabitacionImportForm
    form_class = HabitacionImportForm
    field_mapping = {
        'numero_habitacion': 'numero_habitacion',
        'tipo_habitacion': 'tipo_habitacion',
        'estado': 'estado',
    }
    unique_field = 'numero_habitacion'
    defaults = {'estado': 'DISPONIBLE'}