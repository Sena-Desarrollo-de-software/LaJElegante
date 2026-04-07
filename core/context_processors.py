from django.utils import timezone
from .models import Promocion


def nav_promos_context(request):
    ahora = timezone.now()
    promos = Promocion.objects.filter(
        estado='PUBLICADO',
        tipo__in=['NAVBAR', 'AMBOS'],
        orden_navbar__isnull=False,
        fecha_inicio__lte=ahora,
        fecha_fin__gte=ahora,
    ).order_by('orden_navbar')

    return {'promos': promos}
