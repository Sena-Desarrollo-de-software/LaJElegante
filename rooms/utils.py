from datetime import time
from core.utils import combinar_fecha_hora, validar_anticipacion, validar_modificacion, validar_no_expirado
from core.constants import TIEMPO_LIMITE_HABITACION_HORAS

def obtener_fecha_checkin(fecha_inicio):
    """Obtiene la fecha y hora exacta de check-in (3:00 PM)"""
    return combinar_fecha_hora(fecha_inicio, time(15, 0))

def validar_tiempo_reserva_nueva(fecha_inicio):
    """Valida tiempo límite para nueva reserva"""
    fecha_checkin = obtener_fecha_checkin(fecha_inicio)
    validar_anticipacion(fecha_checkin, TIEMPO_LIMITE_HABITACION_HORAS)

def validar_tiempo_modificacion_reserva(fecha_inicio):
    """Valida tiempo límite para modificación de reserva"""
    fecha_checkin = obtener_fecha_checkin(fecha_inicio)
    validar_modificacion(fecha_checkin, TIEMPO_LIMITE_HABITACION_HORAS)

def validar_fechas_no_expiradas(fecha_inicio):
    """Valida que la reserva no sea en fecha pasada"""
    fecha_checkin = obtener_fecha_checkin(fecha_inicio)
    validar_no_expirado(fecha_checkin)