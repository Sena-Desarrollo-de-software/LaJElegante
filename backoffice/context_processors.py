from .constants import SIDEBAR_CONFIG

MODEL_META = {
    'dashboard': {'label': 'Dashboard', 'icon': 'bi-house-door-fill', 'app': 'backoffice', 'url_name': 'dashboard'},
    'tarifa': {'label': 'Tarifas', 'icon': 'bi-cash', 'app': 'finance', 'url_name': 'tarifa_index'},
    'impuesto': {'label': 'Impuestos', 'icon': 'bi-receipt', 'app': 'finance', 'url_name': 'impuesto_index'},
    'temporada': {'label': 'Temporadas', 'icon': 'bi-calendar', 'app': 'finance', 'url_name': 'temporada_index'},

    'turno': {'label': 'Turnos', 'icon': 'bi-clock', 'app': 'restaurant', 'url_name': 'turno_index'},
    'horario': {'label': 'Horarios', 'icon': 'bi-calendar2-week', 'app': 'restaurant', 'url_name': 'horario_index'},
    'reserva_restaurante': {'label': 'Reservas', 'icon': 'bi-book', 'app': 'restaurant', 'url_name': 'reserva_restaurante_index'},

    'tipohabitacion': {'label': 'Tipos de Habitación', 'icon': 'bi-house', 'app': 'rooms', 'url_name': 'tipo_habitacion_index'},
    'habitacion': {'label': 'Habitaciones', 'icon': 'bi-door-open', 'app': 'rooms', 'url_name': 'habitacion_index'},
    'reserva_habitacion': {'label': 'Reservas', 'icon': 'bi-journal', 'app': 'rooms', 'url_name': 'reserva_habitacion_index'},

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