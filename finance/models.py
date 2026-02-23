from django.db import models
from rooms.models import TipoHabitacion
from core.models import BaseAuditModel

class Temporada(BaseAuditModel):
    class Nombre(models.TextChoices):
        ALTA = 'ALTA' , 'Alta'
        MEDIA = 'MEDIA', 'Media'
        BAJA = 'BAJA', 'Baja'

    nombre = models.CharField(
        max_length = 50,
        choices = Nombre.choices
    )
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    modificador_precio = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        default=1.0,
        help_text="Basado en porcentajes"
    )

class Tarifa(BaseAuditModel):
    class Estado(models.TextChoices):
        VIGENTE = 'VIGENTE', 'Vigente'
        INACTIVA = 'INACTIVA', 'Inactiva'
    
    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.VIGENTE
    )
        
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.CASCADE,
        related_name='tarifas',
        db_column='id_tipo_habitacion'
    )
    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.PROTECT,
        related_name='tarifas',
        db_column='id_temporada'
    )
    
    precio_base = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name="Tarifa base"
    )
    precio_final = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        editable=False,
        help_text="Calculado automáticamente con impuestos"
    )