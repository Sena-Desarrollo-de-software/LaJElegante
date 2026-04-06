from .constants import SIDEBAR_CONFIG, ACTIONS, ROLE_ACTION_KEYS

MODEL_META = {
    'dashboard': {'label': 'Dashboard', 'icon': 'bi-house-door-fill', 'app': 'backoffice', 'url_name': 'dashboard'},
    
    # Core (Reserva contenedor)
    'reserva': {'label': 'Nueva Reserva', 'icon': 'bi-cart-plus', 'app': 'backoffice', 'url_name': 'reserva_index'},

    # Finance
    'tarifa': {'label': 'Tarifas', 'icon': 'bi-cash', 'app': 'finance', 'url_name': 'tarifa_index'},
    'impuesto': {'label': 'Impuestos', 'icon': 'bi-receipt', 'app': 'finance', 'url_name': 'impuesto_index'},
    'temporada': {'label': 'Temporadas', 'icon': 'bi-calendar', 'app': 'finance', 'url_name': 'temporada_index'},

    # Restaurant
    'turno': {'label': 'Turnos', 'icon': 'bi-clock', 'app': 'restaurant', 'url_name': 'turno_index'},
    'horario': {'label': 'Horarios', 'icon': 'bi-calendar2-week', 'app': 'restaurant', 'url_name': 'horario_index'},
    'reserva_restaurante': {'label': 'Reservas Restaurante', 'icon': 'bi-book', 'app': 'restaurant', 'url_name': 'reserva_restaurante_index'},

    # Rooms
    'tipohabitacion': {'label': 'Tipos de Habitación', 'icon': 'bi-house', 'app': 'rooms', 'url_name': 'tipo_habitacion_index'},
    'habitacion': {'label': 'Habitaciones', 'icon': 'bi-door-open', 'app': 'rooms', 'url_name': 'habitacion_index'},
    'reserva_habitacion': {'label': 'Reservas Habitaciones', 'icon': 'bi-journal', 'app': 'rooms', 'url_name': 'reserva_habitacion_index'},

    # Users
    'usuario': {'label': 'Usuarios', 'icon': 'bi-people', 'app': 'users', 'url_name': 'usuario_index'},
    'group': {'label': 'Roles', 'icon': 'bi-shield-lock', 'app': 'users', 'url_name': 'grupo_index'},
}


def sidebar_context(request):
    if not request.user.is_authenticated:
        return {}

    user_groups = set(request.user.groups.values_list('name', flat=True))

    sidebar = []

    for group in user_groups:
        config = SIDEBAR_CONFIG.get(group, {})

        for app, models in config.items():
            for model in models:
                meta = MODEL_META.get(model)

                if not meta:
                    continue

                sidebar.append({
                    'label': meta['label'],
                    'icon': meta['icon'],
                    'url_name': f"{meta['app']}:{meta['url_name']}",
                    'app': meta['app'],
                })

    # evitar duplicados
    unique_sidebar = {item['url_name']: item for item in sidebar}.values()

    return {
        'sidebar_items': list(unique_sidebar),
        'is_admin': 'Administrador' in user_groups,
    }

def shortcut_action_context(request):
    if not request.user.is_authenticated:
        return {}

    user_groups = set(request.user.groups.values_list('name', flat=True))

    action_keys = set()

    for group in user_groups:
        keys = ROLE_ACTION_KEYS.get(group, [])
        action_keys.update(keys)

    shortcuts = []
    for key in action_keys:
        action = ACTIONS.get(key)

        if not action:
            continue

        shortcuts.append({
            'label': action['label'],
            'icon': action['icon'],
            'url_name': action['url_name'],
            'color': action['color']
        })

    # se organiza en orden opcional
    shortcuts = sorted(shortcuts, key=lambda x: x['label'])

    return {
        'shortcuts': shortcuts
    }