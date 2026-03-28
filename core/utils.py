#Archivo para utilidades del sistema para logica de negocio
# === UTILIDADES DE TIEMPO ===
from django.utils import timezone
from datetime import timedelta, datetime

def ahora():
    return timezone.now()

def dentro_de(horas):
    return timedelta(hours=horas)

def combinar_fecha_hora(fecha,hora):
    return timezone.make_aware(datetime.combine(fecha,hora))

# === UTILIDADES PARA SERVICIOS ===
from .constants import SERVICIOS_CONFIG

def get_servicios_activos():
    """Retorna los servicios activos para calcular total"""
    return [s for s in SERVICIOS_CONFIG if s.get('activo', True)]