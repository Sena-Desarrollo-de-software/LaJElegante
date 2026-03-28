#Archivo para constantes globales del sistema para logica de negocio
# === CORE ===
SERVICIOS_CONFIG = [
    {
        'app': 'rooms',
        'model': 'ReservaHabitacion',
        'related_name': 'reservahabitaciones',
        'verbose_name': 'Habitaciones',
        'activo': True,
    },
    {
        'app': 'restaurant',
        'model': 'ReservaRestaurante',
        'related_name': 'reservarestaurantes',
        'verbose_name': 'Restaurante',
        'activo': True,
    },
]
# === RESTAURANTE ===
TIEMPO_LIMITE_RESTAURANTE_HORAS = 3
CAPACIDAD_MAXIMA_TURNO = 50

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