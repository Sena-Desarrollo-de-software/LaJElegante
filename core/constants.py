#Archivo para constantes globales del sistema para logica de negocio
# === CORE ===
SERVICIOS_CONFIG = [
    {
        'app': 'rooms',
        'model': 'ReservaHabitacion',
        'related_name': 'reserva_habitaciones',
        'verbose_name': 'Habitaciones',
        'activo': True,
    },
    {
        'app': 'restaurant',
        'model': 'ReservaRestaurante',
        'related_name': 'reserva_restaurantes',
        'verbose_name': 'Restaurante',
        'activo': True,
    },
]
# === FINANCE ===
SERVICIOS_TARIFABLES = {
    ('restaurant', 'horario'): {
        'model': 'Horario',
        'emoji': '🍽️',
        'nombre': 'Restaurante'
    },
    ('rooms', 'tipohabitacion'): {
        'model': 'TipoHabitacion',
        'emoji': '🛏️',
        'nombre': 'Habitación'
    },
    # Agregar nuevos servicios aquí:
    # ('spa', 'spaservice'): {
    #     'model': 'SpaService',
    #     'emoji': '💆',
    #     'nombre': 'Spa'
    # },
}