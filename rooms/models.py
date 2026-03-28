from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from core.models import BaseAuditModel, ReservaServicio
from core.utils import calcular_dias, validar_capacidad, validar_fechas
from finance.models import get_tarifa_vigente
from .utils import validar_tiempo_reserva_nueva,validar_tiempo_modificacion_reserva,validar_fechas_no_expiradas

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
    descripcion = models.TextField(blank=True, verbose_name="descripción")
    capacidad_maxima = models.PositiveIntegerField(verbose_name="capacidad máxima")

    class Meta:
        verbose_name = "tipo de habitación"
        verbose_name_plural = "tipos de habitaciones"

    def __str__(self):
        return f"{self.get_nombre_tipo_display()} (cap. {self.capacidad_maxima})"


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
        ("DISPONIBLE", "disponible"),
        ("MANTENIMIENTO", "mantenimiento"),
        ("OCUPADA", "ocupada"),
        ("RESERVADA", "reservada"),
    ]
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_HABITACION_CHOICES,
        default="DISPONIBLE",
        verbose_name="estado de la habitación"
    )

    class Meta:
        verbose_name = "habitación"
        verbose_name_plural = "habitaciones"

    def __str__(self):
        return f"Habitación {self.numero_habitacion} - {self.get_estado_display()}"

    def disponible_en_fechas(self, fecha_inicio, fecha_fin, reserva_id=None):
        """Verifica si la habitación está disponible en un rango de fechas"""
        if self.estado in ['MANTENIMIENTO', 'OCUPADA']:
            return False

        reservas = ReservaHabitacion.objects.filter(
            habitacion=self,
            fecha_inicio__lt=fecha_fin,
            fecha_fin__gt=fecha_inicio,
            estado__in=['PENDIENTE', 'CONFIRMADA']
        )
        if reserva_id:
            reservas = reservas.exclude(id=reserva_id)

        return not reservas.exists()


class ReservaHabitacion(ReservaServicio):
    habitacion = models.ForeignKey(
        Habitacion,
        on_delete=models.PROTECT,
        related_name='reservas',
        verbose_name="habitación"
    )
    fecha_inicio = models.DateField(verbose_name="fecha de entrada")
    fecha_fin = models.DateField(verbose_name="fecha de salida")
    cantidad_personas = models.PositiveIntegerField(verbose_name="cantidad de personas")

    # Campos calculados
    cantidad_noches = models.PositiveIntegerField(editable=False, default=0)

    class Meta:
        verbose_name = "reserva de habitación"
        verbose_name_plural = "reservas de habitaciones"
        indexes = [
            models.Index(fields=['fecha_inicio', 'fecha_fin']),
            models.Index(fields=['habitacion', 'fecha_inicio', 'fecha_fin']),
        ]

    def __str__(self):
        return f"Reserva Hab #{self.id} - Hab {self.habitacion.numero_habitacion} ({self.fecha_inicio} al {self.fecha_fin})"

    def clean(self):
        """Validaciones básicas antes de guardar"""
        super().clean()
        validar_fechas(self.fecha_inicio, self.fecha_fin)
        validar_capacidad(self.cantidad_personas, self.habitacion.tipo_habitacion.capacidad_maxima)
        validar_fechas_no_expiradas(self.fecha_inicio)

    def _validar_reserva_nueva(self):
        """Validaciones exclusivas para nueva reserva"""
        validar_tiempo_reserva_nueva(self.fecha_inicio)

        if not self.habitacion.disponible_en_fechas(self.fecha_inicio, self.fecha_fin):
            raise ValidationError("La habitación no está disponible en esas fechas")

    def _validar_modificacion(self, original):
        """Validaciones exclusivas para modificación de reserva"""
        validar_tiempo_modificacion_reserva(self.fecha_inicio)

        # Si cambió de habitación o fechas, verificar disponibilidad
        if (original.habitacion_id != self.habitacion_id or
            original.fecha_inicio != self.fecha_inicio or
            original.fecha_fin != self.fecha_fin):

            if not self.habitacion.disponible_en_fechas(
                self.fecha_inicio, self.fecha_fin, self.pk
            ):
                raise ValidationError("La habitación no está disponible en las nuevas fechas")

    def get_tarifa_vigente(self):
        """Obtiene tarifa vigente para el tipo de habitación en la fecha de inicio"""
        content_type = ContentType.objects.get_for_model(TipoHabitacion)

        return get_tarifa_vigente(
            servicio_tipo=content_type,
            servicio_id=self.habitacion.tipo_habitacion_id,
            fecha=self.fecha_inicio
        )

    def calcular_precio(self):
        """Calcula precio total basado en tarifa vigente"""
        self.cantidad_noches = calcular_dias(self.fecha_inicio, self.fecha_fin)

        tarifa = self.get_tarifa_vigente()
        if not tarifa:
            raise ValidationError("No hay tarifa vigente para estas fechas")

        self.tarifa_aplicada = tarifa
        self.precio_unitario = tarifa.precio_final  # precio por noche
        self.precio_total = (self.precio_unitario * self.cantidad_noches) - self.descuento

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()  # Ejecuta clean()

            if self.pk:
                anterior = ReservaHabitacion.objects.select_for_update().get(pk=self.pk)
                self._validar_modificacion(anterior)
            else:
                self._validar_reserva_nueva()

            self.calcular_precio()
            super().save(*args, **kwargs)