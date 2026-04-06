from django.db.models import Sum
from django.apps import apps

from core.models import Reserva
from restaurant.models import Turno
from core.utils import ahora
from core.constants import SERVICIOS_CONFIG
from .constants import DASHBOARD_WIDGETS, ROLE_WIDGET_KEYS

class DashboardQuery:
    @staticmethod
    def _get_reserva_habitacion_model():
        for s in SERVICIOS_CONFIG:
            if s['model'] == 'ReservaHabitacion':
                return apps.get_model(s['app'], s['model'])
        return None

    @staticmethod
    def checkins_hoy():
        hoy = ahora().date()
        model_ = DashboardQuery._get_reserva_habitacion_model()

        if not model_:
            return []

        return list(
            model_.objects.filter(
                fecha_inicio=hoy
            ).values(
                "id",
                "reserva__usuario__username",
                "habitacion__numero_habitacion"
            )
        )

    @staticmethod
    def checkouts_hoy():
        hoy = ahora().date()
        model_ = DashboardQuery._get_reserva_habitacion_model()

        if not model_:
            return []

        return list(
            model_.objects.filter(
                fecha_fin=hoy
            ).values(
                "id",
                "reserva__usuario__username",
                "habitacion__numero_habitacion"
            )
        )

    @staticmethod
    def personas_en_hotel():
        hoy = ahora().date()
        model_ = DashboardQuery._get_reserva_habitacion_model()

        if not model_:
            return 0

        reservas = model_.objects.filter(
            fecha_inicio__lte=hoy,
            fecha_fin__gte=hoy
        )

        return reservas.aggregate(
            total=Sum('cantidad')
        )['total'] or 0

    @staticmethod
    def proximo_turno_restaurante():
        ahora_time = ahora().time()
        hoy = ahora().date()

        turno = (
            Turno.objects.select_related('horario')
            .filter(
                fecha=hoy,
                horario__hora_inicio__gte=ahora_time
            )
            .order_by('horario__hora_inicio')
            .first()
        )

        if not turno:
            return None

        return {
            "turno": turno.horario.turno,
            "hora_inicio": turno.horario.hora_inicio,
            "ocupados": turno.quorum,
            "capacidad": turno.capacidad_efectiva,
        }

    @staticmethod
    def reservas_hoy():
        hoy = ahora().date()

        return Reserva.objects.filter(
            fecha_reserva__date=hoy
        ).count()
    
    @staticmethod
    def ingresos_reales_hoy():
        hoy = ahora().date()

        return sum(
            r.total for r in Reserva.objects.filter(
                fecha_reserva__date=hoy,
                estado__in=["CONFIRMADA", "COMPLETADA"]
            )
        )


    @staticmethod
    def penalizaciones_hoy():
        hoy = ahora().date()

        return sum(
            getattr(r, "penalizacion", 0)
            for r in Reserva.objects.filter(
                fecha_reserva__date=hoy,
                estado="CANCELADA"
            )
        )


    @staticmethod
    def ingresos_totales_hoy():
        return (
            DashboardQuery.ingresos_reales_hoy() +
            DashboardQuery.penalizaciones_hoy()
        )

    @staticmethod
    def resumen_general():
        return {
            "reservas_hoy": DashboardQuery.reservas_hoy(),
            "ingresos_reales": float(DashboardQuery.ingresos_reales_hoy()),
            "penalizaciones": float(DashboardQuery.penalizaciones_hoy()),
            "ingresos_totales": float(DashboardQuery.ingresos_totales_hoy()),
            "personas_hotel": DashboardQuery.personas_en_hotel(),
            "checkins": DashboardQuery.checkins_hoy(),
            "checkouts": DashboardQuery.checkouts_hoy(),
            "restaurante": DashboardQuery.proximo_turno_restaurante(),
        }
    
class DashboardService:

    @staticmethod
    def get_dashboard_for_user(user):

        if not user.is_authenticated:
            return {}

        user_groups = set(user.groups.values_list('name', flat=True))

        widget_keys = set()

        for group in user_groups:
            widget_keys.update(ROLE_WIDGET_KEYS.get(group, []))

        data = {}

        for key in widget_keys:
            widget = DASHBOARD_WIDGETS.get(key)

            if not widget:
                continue

            method = getattr(DashboardQuery, widget['method'], None)

            if not method:
                continue

            data[key] = {
                "label": widget["label"],
                "icon": widget["icon"],
                "color": widget["color"],
                "value": method()
            }

        return data