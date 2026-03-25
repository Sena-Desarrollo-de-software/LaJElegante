from django.db import models
from core.models import BaseAuditModel, ReservaServicio

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
        unique=True)

    hora_inicio = models.TimeField(
        verbose_name='Inicio del horario'
    )

    hora_fin = models.TimeField(
        verbose_name='Fin del horario'
    )

    precio_por_persona = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        verbose_name='Precio por persona - Buffet')

    capacidad_maxima = models.PositiveIntegerField(
        verbose_name='Capacidad maxima de esta franja'
    )

    class Meta:
        verbose_name = "horario"
        verbose_name_plural = "horarios"
        indexes = [
            models.Index(fields=['turno']),
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

    cantidad_personas = models.PositiveIntegerField(
        default=0,
        verbose_name='cantidad personas'
    )

    class Meta:
        verbose_name = 'turno'
        verbose_name_plural = 'turnos'
        unique_together = ['fecha','horario']
        indexes = [
            models.Index(fields=['fecha','horario'])
        ]
    
    @property
    def capacidad_disponible(self):
        return self.horario.capacidad_maxima - self.cantidad_personas
    
    def disponible(self, personas):
        return self.capacidad_disponible >= personas
    
    def __str__(self):
        return f"{self.horario} - {self.fecha} ({self.cantidad_personas} / {self.horario.capacidad_maxima})"

# === RESERVA RESTAURANTE ===
class ReservaRestaurante(ReservaServicio):
    turno = models.ForeignKey(
        Turno,
        on_delete=models.PROTECT,
        related_name='reservas'
    )

    def save(self, *args, **kwargs): #Al guardar actualiza la capacidad del turno
        if self.pk:
            anterior = ReservaRestaurante.objects.get(pk= self.pk)
            diferencia = self.numero_personas - anterior.numero_personas
        else:
            diferencia = self.numero_personas
        
        self.turno.cantidad_personas += diferencia
        self.turno.save()

        super().save(*args,**kwargs)
    
    def get_tarifa_vigente(self):
        from django.contrib.contenttypes.models import ContentType
        from finance.models import get_tarifa_vigente
        
        content_type = ContentType.objects.get_for_model(Horario)

        return get_tarifa_vigente(
            servicio_tipo=content_type,
            servicio_id=self.turno.horario_id,
            fecha=self.turno.fecha
        )

    def calcular_precio(self): 
        tarifa = self.get_tarifa_vigente()

        if not tarifa:
            self.precio_total = 0
            self.precio_unitario = 0
            return
        self.tarifa_aplicada = tarifa
        self.precio_final = tarifa.precio_final
        self.precio_total = (self.precio_unitario * self.cantidad) - self.descuento #Comentario para recordar agregar recargo, descuento por ahora es un numero fijo