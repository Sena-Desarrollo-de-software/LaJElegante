from django.db import models
from django.core.exceptions import ValidationError
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

    nombre_tipo = models.CharField(
        max_length=20, 
        choices=NOMBRE_TIPO_CHOICES,
        verbose_name="nombre del tipo"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="descripción"
    )
    capacidad_maxima = models.PositiveIntegerField(
        verbose_name="capacidad máxima"
    )

    class Meta:
        verbose_name = "tipo de habitación"
        verbose_name_plural = "tipos de habitaciones"

    def __str__(self):
        return f"{self.get_nombre_tipo_display()} (cap. {self.capacidad_maxima})"


# === Habitacion ===
class Habitacion(BaseAuditModel):
    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.PROTECT,
        related_name="habitaciones",
        verbose_name="tipo de habitación"
    )

    numero_habitacion = models.PositiveIntegerField(
        unique=True,
        verbose_name="número de habitación"
    )

    ESTADO_HABITACION_CHOICES = [
        ("EN_SERVICIO", "en servicio"),
        ("MANTENIMIENTO", "mantenimiento"),
        ("OCUPADA", "ocupada"),
    ]

    estado_habitacion = models.CharField(
        max_length=20,
        choices=ESTADO_HABITACION_CHOICES,
        default="EN_SERVICIO",
        verbose_name="estado de la habitación"
    )

    class Meta:
        verbose_name = "habitación"
        verbose_name_plural = "habitaciones"

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.get_estado_habitacion_display()}"

# === ReservaHabitacion ===
class ReservaHabitacion(BaseAuditModel):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservas_habitacion",
        verbose_name="cliente"
    )

    class Meta:
        verbose_name = "reserva de habitación"
        verbose_name_plural = "reservas de habitaciones"

    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.username}"

# === DetallesReservaHabitacion ===
class DetallesReservaHabitacion(BaseAuditModel):
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name="detalles_reserva"
    )

    reserva_habitacion = models.ForeignKey(
        ReservaHabitacion,
        on_delete=models.CASCADE,
        related_name="detalles"
    )

    fecha_inicio = models.DateField(verbose_name="fecha de inicio")
    fecha_fin = models.DateField(verbose_name="fecha de fin")

    cantidad_personas = models.PositiveIntegerField(verbose_name="cantidad de personas")
    
    # Relación con tarifa (opcional, se puede calcular)
    tarifa_aplicada = models.ForeignKey(
        "finance.Tarifa", # Hay que importar con String FK para evitar problemas circular (las entidades se necesitan mutuamente, infinitamente)
        on_delete=models.PROTECT,
        null=True,
        editable=False,
        verbose_name="tarifa aplicada"
    )
    
    precio_por_noche = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        editable=False,
        verbose_name="precio por noche"
    )
    
    cantidad_noches = models.PositiveIntegerField(
        editable=False,
        verbose_name="cantidad de noches"
    )
    
    descuento_aplicado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0,
        verbose_name="descuento adicional"
    )
    
    recargo_aplicado = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.0,
        verbose_name="recargo adicional"
    )
    
    precio_total = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        editable=False,
        verbose_name="precio total"
    )

    observacion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "detalle de reserva"
        verbose_name_plural = "detalles de reservas"

    def get_tarifa_vigente(self):
        from finance.models import Tarifa  # Import local para evitar circular
        
        tipo_hab = self.habitacion.tipo_habitacion
        
        # Buscar tarifa VIGENTE para este tipo y que cubra la fecha
        tarifas = Tarifa.objects.filter(
            tipo_habitacion=tipo_hab,
            estado='VIGENTE',
            temporada__fecha_inicio__lte=self.fecha_inicio,
            temporada__fecha_fin__gte=self.fecha_inicio
        ).select_related('temporada')
        
        if tarifas.exists():
            return tarifas.first()
        return None

    def clean(self):
        if self.fecha_inicio and self.fecha_fin:
            if self.fecha_inicio >= self.fecha_fin:
                raise ValidationError("La fecha de fin debe ser posterior a la fecha de inicio")

    def save(self, *args, **kwargs):
        if not self.fecha_inicio or not self.fecha_fin:
            raise ValidationError("Debe especificar fecha de inicio y fin")
        
        delta = self.fecha_fin - self.fecha_inicio
        self.cantidad_noches = delta.days
        
        tarifa = self.get_tarifa_vigente()
        if not tarifa:
            raise ValidationError("No hay tarifa vigente para esta fecha")
        
        self.tarifa_aplicada = tarifa
        self.precio_por_noche = tarifa.precio_final
        
        base = self.precio_por_noche * self.cantidad_noches
        self.precio_total = base - self.descuento_aplicado + self.recargo_aplicado
        
        super().save(*args, **kwargs)
