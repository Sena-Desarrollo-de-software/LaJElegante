from django.db import models

class BaseAuditModel(models.Model):
    is_active = models.BooleanField(default=True)  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

# === Mesa ===
class Mesa(BaseAuditModel):
    numero_mesa = models.SmallIntegerField()
    capacidad = models.SmallIntegerField()
    zona = models.CharField(max_length = 50)
    ubicacion_detalle = models.CharField(max_length = 150)

# === Reserva Restaurante ===
class ReservaRestaurante(BaseAuditModel):
    #Referencia temporal a cliente
    cliente_id = models.PositiveIntegerField()
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