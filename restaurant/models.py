from django.db import models
from core.models import BaseAuditModel
from users.models import Usuario

# === Mesa ===
class Mesa(BaseAuditModel):
    numero_mesa = models.SmallIntegerField(
        verbose_name="número de mesa"
    )
    capacidad = models.SmallIntegerField(
        verbose_name="capacidad de personas"
    )
    zona = models.CharField(
        max_length=50,
        verbose_name="zona del restaurante"
    )
    ubicacion_detalle = models.CharField(
        max_length=150,
        verbose_name="ubicación detallada"
    )

    class Meta:
        verbose_name = "mesa"
        verbose_name_plural = "mesas"
        ordering = ['zona', 'numero_mesa']
        unique_together = ['numero_mesa', 'zona']

    def __str__(self):
        return f"Mesa {self.numero_mesa} - {self.zona} ({self.capacidad} pers.)"

# === Reserva Restaurante ===
class ReservaRestaurante(BaseAuditModel):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservas_restaurante",
        verbose_name="cliente"
    )

    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="mesa asignada"
    )
    
    hora_reserva = models.TimeField(
        verbose_name="hora de la reserva"
    )
    
    numero_personas = models.SmallIntegerField(
        verbose_name="número de personas"
    )

    ESTADO_RESERVA_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
    ]

    estado_reserva = models.CharField(
        max_length=20,
        choices=ESTADO_RESERVA_CHOICES,
        default='PENDIENTE',
        verbose_name="estado de la reserva"
    )

    class Meta:
        verbose_name = "reserva de restaurante"
        verbose_name_plural = "reservas de restaurante"
        ordering = ['-created_at', 'hora_reserva']
        indexes = [
            models.Index(fields=['estado_reserva', 'hora_reserva']),
        ]

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.username} - {self.mesa}"

    def get_estado_display_color(self):
        estados_color = {
            'PENDIENTE': 'Pendiente',
            'CONFIRMADA': 'Confirmada',
            'CANCELADA': 'Cancelada',
        }
        return estados_color.get(self.estado_reserva, self.estado_reserva)

    def get_hora_formateada(self):
        """Devuelve la hora en formato HH:MM AM/PM"""
        return self.hora_reserva.strftime('%I:%M %p')

    def capacidad_suficiente(self):
        return self.mesa.capacidad >= self.numero_personas
    capacidad_suficiente.boolean = True
    capacidad_suficiente.short_description = 'Capacidad suficiente'

    def verificar_disponibilidad(self, fecha):
        return not ReservaRestaurante.objects.filter(
            mesa=self.mesa,
            created_at__date=fecha,
            estado_reserva__in=['PENDIENTE', 'CONFIRMADA']
        ).exclude(id=self.id).exists()