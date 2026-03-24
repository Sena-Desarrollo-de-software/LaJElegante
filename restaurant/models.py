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

    numero_personas = models.PositiveIntegerField(
        verbose_name='número de personas'
    )

    ESTADO_RESERVA_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]

    estado = models.CharField(
        max_length=20,
        choices=ESTADO_RESERVA_CHOICES,
        default='PENDIENTE',        
        verbose_name='estado reserva'
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
    
    def get_tarifa_vigente(self): #Faltan modelos de finance para servicios
        return super().get_tarifa_vigente()
    
    def calcular_precio(self): #Faltan modelos de finance para servicios
        return super().calcular_precio