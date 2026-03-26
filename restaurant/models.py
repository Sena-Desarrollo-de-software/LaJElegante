from django.db import models, transaction
from core.models import BaseAuditModel, ReservaServicio
from django.core.exceptions import ValidationError
from core.utils import ahora,dentro_de,combinar_fecha_hora
from core.constants import TIEMPO_LIMITE_RESTAURANTE_HORAS, CAPACIDAD_MAXIMA_TURNO

# === HORARIO ===
class Horario(BaseAuditModel):
    TURNO_CHOICES = [
        ('MAÑANA','Desayuno'),
        ('TARDE','Almuerzo'),
        ('NOCHE','Cena'),
    ]

    turno = models.CharField(
        max_length=10, 
        choices=TURNO_CHOICES,
        verbose_name='Franja Horaria',
        unique=True
    )

    hora_inicio = models.TimeField(verbose_name='Inicio del horario')

    hora_fin = models.TimeField(verbose_name='Fin del horario')

    capacidad_maxima = models.PositiveIntegerField(
        default=CAPACIDAD_MAXIMA_TURNO,
        verbose_name='Capacidad maxima de esta franja horaria'
    )

    class Meta:
        verbose_name = "configuración de horario"
        verbose_name_plural = "conguración de horarios"
        indexes = [
            models.Index(fields=['turno','capacidad_maxima']),
        ]
    
    def __str__(self):
        return f"{self.get_turno_display()} {self.hora_inicio} - {self.hora_fin}"

class Turno(BaseAuditModel):
    horario = models.ForeignKey(
        Horario,
        on_delete=models.PROTECT,
        related_name='turnos'
    )

    fecha = models.DateField(
        verbose_name='fecha'
    )

    quorum = models.PositiveIntegerField(
        default=0,
        verbose_name='Personas reservadas'
    )

    #Campos para sobreescritura de configuración de horarios por si es necesaria
    capacidad_maxima = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name='Capacidad maxima',
        help_text='Sobreescribe capacidad maxima de los horarios (dejar vacio si no es necesario)'
    )

    class Meta:
        verbose_name = 'turno'
        verbose_name_plural = 'turnos'
        unique_together = ['fecha','horario']
        indexes = [
            models.Index(fields=['fecha','horario','capacidad_maxima'])
        ]
    
    @property
    def capacidad_disponible(self):
        return self.horario.capacidad_maxima - self.quorum

    @property
    def capacidad_efectiva(self):
        return self.capacidad_maxima or self.horario.capacidad_maxima
    
    def disponible(self, personas):
        return self.capacidad_disponible >= personas
    
    def reservar(self, personas):
        if personas <= 0:
            return
        if not self.disponible(personas):
            raise ValidationError(f"No hay cupo disponible. Solo quedan {self.capacidad_disponible} lugares")
        self.quorum += personas
        self.save()
    
    def cancelar(self, personas):
        if personas <= 0:
            return
        self.quorum -= personas
        self.save()
    
    def ajustar(self, personas_anteriores, personas_nuevas):
        diferencia = personas_nuevas - personas_anteriores
        if diferencia > 0:
            self.reservar(diferencia)
        elif diferencia < 0:
            self.cancelar(-diferencia)
    
    def __str__(self):
        return f"{self.horario} - {self.fecha} ({self.quorum} / {self.horario.capacidad_maxima})"

# === RESERVA RESTAURANTE ===
class ReservaRestaurante(ReservaServicio):
    turno = models.ForeignKey(
        Turno,
        on_delete=models.PROTECT,
        related_name='reservas',
        null=True,
        blank=True
    )

    def _validar_modificacion(self, original):
        if not original:
            return
        
        fecha_reserva = combinar_fecha_hora(
            self.turno.fecha,
            self.turno.horario.hora_inicio
        )

        limite = fecha_reserva - dentro_de(TIEMPO_LIMITE_RESTAURANTE_HORAS)

        if ahora() > limite:
            raise ValidationError(f"Las reservas solo pueden modificarse hasta {TIEMPO_LIMITE_RESTAURANTE_HORAS} horas antes del servicio.")
        
        if fecha_reserva < ahora():
            raise ValidationError("No se puede reservar en una fecha pasada.")
        
        if ahora() > fecha_reserva:
            raise ValidationError("No se puede modificar una reserva que ha expirado.")
    
    def get_tarifa_vigente(self):
        from django.contrib.contenttypes.models import ContentType
        from finance.models import get_tarifa_vigente
        
        content_type = ContentType.objects.get_for_model(Horario)

        return get_tarifa_vigente(
            servicio_tipo=content_type,
            servicio_id=self.turno.horario_id,
            fecha=self.turno.fecha
        )

    def cancelar(self):
        with transaction.atomic():
            self.estado = 'CANCELADA'
            self.save()
            self.turno.cancelar(self.cantidad)

    def confirmar(self):
        with transaction.atomic():
            self.estado = 'CONFIRMADA'
            self.save()

    def completar(self):
        with transaction.atomic():
            self.estado = 'COMPLETADA'
            self.save()

    def save(self, *args, **kwargs):
        with transaction.atomic():
            turno = Turno.objects.select_for_update().get(pk=self.turno_id)
            if self.pk:
                anterior = ReservaRestaurante.objects.select_for_update().get(pk=self.pk)
                self._validar_modificacion(anterior)

                if anterior.turno_id != self.turno_id:
                    anterior.estado = 'CANCELADA'
                    anterior.save()
                    anterior.turno.cancelar(anterior.cantidad)                
                    turno.reservar(self.cantidad)

                elif anterior.cantidad != self.cantidad:
                    turno.ajustar(anterior.cantidad, self.cantidad)
            else:
                turno.reservar(self.cantidad)
        super().save(*args, **kwargs)
                
    def calcular_precio(self): 
        tarifa = self.get_tarifa_vigente()
        if not tarifa:
            raise ValidationError("No hay tarifa vigente para este horario")
        
        self.tarifa_aplicada = tarifa
        self.precio_unitario = tarifa.precio_final
        self.precio_total = (self.precio_unitario * self.cantidad) - self.descuento #Comentario para recordar agregar recargo, descuento por ahora es un numero fijo