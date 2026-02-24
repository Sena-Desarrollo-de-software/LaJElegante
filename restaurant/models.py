from django.db import models
from core.models import BaseAuditModel
from users.models import Usuario

# === Mesa ===
class Mesa(BaseAuditModel):
    numero_mesa = models.SmallIntegerField()
    capacidad = models.SmallIntegerField()
    zona = models.CharField(max_length = 50)
    ubicacion_detalle = models.CharField(max_length = 150)

# === Reserva Restaurante ===
class ReservaRestaurante(BaseAuditModel):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservas_restaurante",
        verbose_name="Cliente"
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete = models.CASCADE,
        related_name = 'reserva', 
    )
    hora_reserva = models.TimeField()
    numero_personas = models.SmallIntegerField()

    ESTADO_RESERVA_CHOICES = [
        ('PENDIENTE','pendiente'),
        ('CONFIRMADA','confirmada'),
        ('CANCELADA','cancelada'),
    ]

    estado_reserva = models.CharField(
        max_length = 20,
        choices = ESTADO_RESERVA_CHOICES,
        default =  'PENDIENTE',
    )