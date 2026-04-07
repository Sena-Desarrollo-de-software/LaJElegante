SIDEBAR_CONFIG = {
    'Administrador': {
        'dashboard': ['dashboard', 'reserva'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reserva_restaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reserva_habitacion'],
        'users': ['usuario', 'group'],
        'admin_panel': ['admin_panel'],
    },
    'Gerente General': {
        'dashboard': ['dashboard', 'reserva'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reserva_restaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reserva_habitacion'],
    },
    'Gerente de Habitaciones': {
        'dashboard': ['dashboard', 'reserva'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'rooms': ['tipohabitacion', 'habitacion', 'reserva_habitacion'],
    },
    'Gerente de Comidas y Bebidas': {
        'dashboard': ['dashboard', 'reserva'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reserva_restaurante'],
    },
    'Asistente Administrativo': {
        'dashboard': ['dashboard', 'reserva'],
        'finance': ['tarifa', 'impuesto', 'temporada'],
        'restaurant': ['turno', 'horario', 'reserva_restaurante'],
        'rooms': ['tipohabitacion', 'habitacion', 'reserva_habitacion'],
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

DASHBOARD_WIDGETS = {
    'RESERVAS_HOY': {
        'label': 'Reservas hoy',
        'method': 'reservas_hoy',
        'icon': 'bi-calendar-check',
        'color': 'primary',
    },
    'INGRESOS_REALES': {
        'label': 'Ingresos reales',
        'method': 'ingresos_reales_hoy',
        'icon': 'bi-cash-stack',
        'color': 'success',
    },
    'PENALIZACIONES': {
        'label': 'Penalizaciones',
        'method': 'penalizaciones_hoy',
        'icon': 'bi-exclamation-triangle',
        'color': 'warning',
    },
    'INGRESOS_TOTALES': {
        'label': 'Ingresos totales',
        'method': 'ingresos_totales_hoy',
        'icon': 'bi-graph-up',
        'color': 'primary',
    },
    'PERSONAS_HOTEL': {
        'label': 'Personas alojadas',
        'method': 'personas_en_hotel',
        'icon': 'bi-people',
        'color': 'info',
    },
    'CHECKINS_HOY': {
        'label': 'Check-ins',
        'method': 'checkins_hoy',
        'icon': 'bi-box-arrow-in-right',
        'color': 'primary',
    },
    'CHECKOUTS_HOY': {
        'label': 'Check-outs',
        'method': 'checkouts_hoy',
        'icon': 'bi-box-arrow-left',
        'color': 'secondary',
    },
    'RESTAURANTE_TURNO': {
        'label': 'Turno restaurante',
        'method': 'proximo_turno_restaurante',
        'icon': 'bi-cup-hot',
        'color': 'warning',
    },
}

ROLE_WIDGET_KEYS = {

    'Administrador': [
        'RESERVAS_HOY',
        'INGRESOS_REALES',
        'PENALIZACIONES',
        'INGRESOS_TOTALES',
        'PERSONAS_HOTEL',
        'CHECKINS_HOY',
        'CHECKOUTS_HOY',
        'RESTAURANTE_TURNO',
    ],

    'Gerente General': [
        'RESERVAS_HOY',
        'INGRESOS_REALES',
        'PENALIZACIONES',
        'INGRESOS_TOTALES',
        'PERSONAS_HOTEL',
        'RESTAURANTE_TURNO',
    ],

    'Gerente de Habitaciones': [
        'PERSONAS_HOTEL',
        'CHECKINS_HOY',
        'CHECKOUTS_HOY',
    ],

    'Gerente de Comidas y Bebidas': [
        'RESTAURANTE_TURNO',
    ],

    'Asistente Administrativo': [
        'RESERVAS_HOY',
        'PERSONAS_HOTEL',
        'CHECKINS_HOY',
        'CHECKOUTS_HOY',
        'RESTAURANTE_TURNO',
    ],
}