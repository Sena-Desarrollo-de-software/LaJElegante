#Archivo para utilidades del sistema para logica de negocio
# === UTILIDADES DE TIEMPO ===
from django.utils import timezone
from datetime import timedelta, datetime

def ahora():
    return timezone.now()

def dentro_de(horas):
    return ahora() + timedelta(hours=horas)

def combinar_fecha_hora(fecha,hora):
    return timezone.make_aware(datetime.combine(fecha,hora))