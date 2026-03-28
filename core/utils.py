#Archivo para utilidades del sistema para logica de negocio
# === UTILIDADES DE TIEMPO ===
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.exceptions import ValidationError

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

# ===== VALIDACIONES GENÉRICAS =====
def validar_fechas(fecha_inicio, fecha_fin):
    """Valida que fecha_fin sea posterior a fecha_inicio"""
    if fecha_inicio >= fecha_fin:
        raise ValidationError("La fecha de salida debe ser posterior a la fecha de entrada")

def validar_anticipacion(fecha_evento, horas_limite):
    """Valida que la reserva se haga con anticipación suficiente"""
    fecha_limite = fecha_evento - dentro_de(horas_limite)
    if ahora() > fecha_limite:
        raise ValidationError(
            f"Las reservas deben hacerse con al menos {horas_limite} horas de anticipación"
        )

def validar_modificacion(fecha_evento, horas_limite):
    """Valida que la modificación se haga dentro del tiempo permitido"""
    fecha_limite = fecha_evento - dentro_de(horas_limite)
    if ahora() > fecha_limite:
        raise ValidationError(
            f"Las reservas solo pueden modificarse hasta {horas_limite} horas antes"
        )

def validar_no_expirado(fecha_evento):
    """Valida que la fecha no haya pasado"""
    if fecha_evento < ahora():
        raise ValidationError("No se puede reservar en una fecha pasada")

def calcular_dias(fecha_inicio, fecha_fin):
    """Calcula número de días entre dos fechas"""
    return (fecha_fin - fecha_inicio).days

def validar_capacidad(personas_solicitadas, capacidad_maxima):
    """Valida que no exceda la capacidad máxima"""
    if personas_solicitadas > capacidad_maxima:
        raise ValidationError(
            f"Solo se permiten {capacidad_maxima} personas"
        )