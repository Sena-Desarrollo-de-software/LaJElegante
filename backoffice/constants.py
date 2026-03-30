SIDEBAR_CONFIG = {
    'Administrador': {
        'dashboard': ['dashboard'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reservarestaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reservahabitacion'],
        'users': ['usuario', 'group'],
    },
    'Gerente General': {
        'dashboard': ['dashboard'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reservarestaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reservahabitacion'],
    },
    'Gerente de Habitaciones': {
        'dashboard': ['dashboard'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'rooms': ['tipohabitacion', 'habitacion', 'reservahabitacion'],
    },
    'Gerente de Comidas y Bebidas': {
        'dashboard': ['dashboard'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reservarestaurante'],
    },
    'Asistente Administrativo': {
        'dashboard': ['dashboard'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reservarestaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reservahabitacion'],
    },
}

ACTIONS = {
    'RESERVA_CREATE': {
        'label': 'Crear Reserva',
        'icon': 'bi-plus-circle',
        'url_name': 'backoffice:reserva_create',
        'color': 'primary',
    },
    'RESERVA_LIST': {
        'label': 'Ver Reservas',
        'icon': 'bi-journal',
        'url_name': 'backoffice:reserva_index',
        'color': 'primary',
    },
    'HABITACION_CREATE': {
        'label': 'Nueva Habitación',
        'icon': 'bi-door-open',
        'url_name': 'rooms:habitacion_create',
        'color': 'primary',
    },
    'HABITACION_LIST': {
        'label': 'Habitaciones',
        'icon': 'bi-door-open',
        'url_name': 'rooms:habitacion_index',
        'color': 'primary',
    },
    'TARIFA_CREATE': {
        'label': 'Nueva Tarifa',
        'icon': 'bi-cash',
        'url_name': 'finance:tarifa_create',
        'color': 'primary',
    },
    'TARIFA_LIST': {
        'label': 'Tarifas',
        'icon': 'bi-cash',
        'url_name': 'finance:tarifa_index',
        'color': 'primary',
    },
    'USUARIO_LIST': {
        'label': 'Usuarios',
        'icon': 'bi-people',
        'url_name': 'users:usuario_index',
        'color': 'primary',
    },
    'DASHBOARD': {
        'label': 'Dashboard',
        'icon': 'bi-house-door',
        'url_name': 'backoffice:dashboard',
        'color': 'primary',
    },
    'TURNOS': {
        'label': 'Turnos',
        'icon': 'bi-clock',
        'url_name': 'restaurant:turno_index',
        'color': 'primary',
    },
    'RESERVA_RESTAURANTE_CREATE': {
        'label': 'Nueva Reserva',
        'icon': 'bi-plus-circle',
        'url_name': 'restaurant:reserva_restaurante_create',
        'color': 'primary',
    },
    'RESERVA_RESTAURANTE_LIST': {
        'label': 'Reservas Restaurante',
        'icon': 'bi-book',
        'url_name': 'restaurant:reserva_restaurante_index',
        'color': 'primary',
    },
}

ROLE_ACTION_KEYS = {

    'Administrador': [
        'RESERVA_CREATE',
        'RESERVA_LIST',
        'HABITACION_CREATE',
        'TARIFA_CREATE',
        'USUARIO_LIST',
        'DASHBOARD',
    ],

    'Gerente General': [
        'DASHBOARD',
        'RESERVA_LIST',
        'HABITACION_LIST',
        'TURNOS',
        'TARIFA_LIST',
    ],

    'Gerente de Habitaciones': [
        'RESERVA_CREATE',
        'RESERVA_LIST',
        'HABITACION_LIST',
    ],

    'Gerente de Comidas y Bebidas': [
        'RESERVA_RESTAURANTE_CREATE',
        'RESERVA_RESTAURANTE_LIST',
        'TURNOS',
    ],

    'Asistente Administrativo': [
        'RESERVA_CREATE',
        'RESERVA_LIST',
        'HABITACION_LIST',
        'RESERVA_RESTAURANTE_LIST',
        'TURNOS',
        'TARIFA_LIST',
    ],
}