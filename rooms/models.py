from django.db import models
from core.models import BaseAuditModel
from users.models import Usuario

# === TipoHabitacion ===
class TipoHabitacion(BaseAuditModel):
    NOMBRE_TIPO_CHOICES = [
        ("FAMILIAR", "familiar"),
        ("PAREJA", "pareja"),
        ("BASICA", "basica"),
        ("ESPECIAL", "especial"),
    ]

    nombre_tipo = models.CharField(max_length=20, choices=NOMBRE_TIPO_CHOICES)
    descripcion = models.TextField(blank=True)
    capacidad_maxima = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.get_nombre_tipo_display()} (cap. {self.capacidad_maxima})"


# === Habitacion ===
class Habitacion(BaseAuditModel):
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.PROTECT,
        related_name="habitaciones",
    )

    numero_habitacion = models.PositiveIntegerField(unique=True)

    ESTADO_HABITACION_CHOICES = [
        ("EN_SERVICIO", "en servicio"),
        ("MANTENIMIENTO", "mantenimiento"),
        ("OCUPADA", "ocupada"),
    ]

    estado_habitacion = models.CharField(
        max_length=20,
        choices=ESTADO_HABITACION_CHOICES,
        default="EN_SERVICIO",
    )

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.get_estado_habitacion_display()}"


# === DetallesReservaHabitacion ===
class DetallesReservaHabitacion(BaseAuditModel):
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name="detalles_reserva",
    )

    cantidad_personas = models.PositiveIntegerField()
    cantidad_noches = models.PositiveIntegerField()

    precio_noche = models.DecimalField(max_digits=10, decimal_places=2)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    recargo_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    precio_reserva = models.DecimalField(max_digits=12, decimal_places=2)

    observacion = models.TextField(blank=True)

    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return f"Detalle Reserva #{self.id} - Habitación {self.habitacion.numero_habitacion}"


# === ReservaHabitacion ===
class ReservaHabitacion(BaseAuditModel):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservas_habitacion",
        verbose_name="Cliente"
    )

    detalle_reserva_habitacion = models.OneToOneField(
        DetallesReservaHabitacion,
        on_delete=models.CASCADE,
        related_name="reserva",
    )

    def __str__(self):
        return f"ReservaHabitacion #{self.id} (cliente_id={self.cliente_id})"
