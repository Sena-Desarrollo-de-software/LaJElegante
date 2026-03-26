from django.db import models
from users.models import Usuario
from django.apps import apps

class BaseAuditModel(models.Model):
    is_active = models.BooleanField(default=True)  # Soft delete
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
    # Todas las clases aqui son para manejar el landing page
class Promocion(BaseAuditModel):
    TIPO_PROMOCION_CHOICES = [
        ('NAVBAR', 'Solo navbar (300x85px)'),
        ('PAGINA', 'Solo página completa'),
        ('AMBOS', 'Ambos formatos'),
    ]
    
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('PUBLICADO', 'Publicado'),
    ]
    
    titulo = models.CharField(
        max_length=200,
        verbose_name="título"
    )
    
    descripcion = models.TextField(
        blank=True,
        verbose_name="descripción"
    )
    
    imagen_pequena = models.ImageField(
        upload_to='promociones/navbar/',
        help_text="Tamaño: 300x85px - Para el navbar",
        verbose_name="imagen pequeña"
    )
    
    imagen_grande = models.ImageField(
        upload_to='promociones/landingpage/',
        help_text="Formato 3:4 - Para página de promociones",
        verbose_name="imagen grande"
    )
    
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_PROMOCION_CHOICES,
        default='AMBOS',
        verbose_name="mostrar en"
    )
    
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default='BORRADOR',
        verbose_name="estado"
    )
    
    orden_navbar = models.PositiveIntegerField(
        null=True,
        blank=True,
        unique=True,
        verbose_name="orden en navbar (1-4)",
        help_text="Valor único. Dejar vacío si no va en navbar"
    )
    
    fecha_inicio = models.DateTimeField(
        verbose_name="publicar desde"
    )
    
    fecha_fin = models.DateTimeField(
        verbose_name="publicar hasta"
    )
    
    class Meta:
        verbose_name = "promoción"
        verbose_name_plural = "promociones"
        ordering = ['orden_navbar', '-fecha_inicio']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(orden_navbar__gte=1, orden_navbar__lte=4) | models.Q(orden_navbar__isnull=True),
                name="orden_navbar_rango"
            )
        ]
    
    def __str__(self):
        return self.titulo
    
    def esta_activa(self):
        from django.utils import timezone
        ahora = timezone.now()
        return (
            self.estado == 'PUBLICADO' and
            self.fecha_inicio <= ahora <= self.fecha_fin
        )
    # Todas las clases aqui son para el sistema
class Reserva(BaseAuditModel):
    """
    Contenedor de una reserva que puede incluir múltiples servicios.
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name="reservas"
    )
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PENDIENTE')
    
    class Meta:
        verbose_name = "reserva"
        verbose_name_plural = "reservas"
    
    def __str__(self):
        return f"Reserva #{self.id} - {self.usuario.username}"
    
    @property
    def total(self):
        """
        Calcula el total sumando todos los servicios asociados.
        """
        total = 0
        
        # Configuración de servicios: (app, model_name, related_name)
        servicios_config = [
            ('rooms', 'ReservaHabitacion', 'habitaciones'),
            ('restaurant', 'ReservaRestaurante', 'restaurantes'),
            """
            ('spa', 'ReservaSpa', 'spa'),  # Como agregar futuros modelos de servicios
            ('eventos', 'ReservaEvento', 'eventos'),
            """
        ]
        
        for app, model_name, related_name in servicios_config:
            try:
                # Obtener el modelo usando apps.get_model
                model = apps.get_model(app, model_name)
                
                # Verificar que el modelo existe y que la reserva tiene esa relación
                if model and hasattr(self, related_name):
                    queryset = getattr(self, related_name).all()
                    total += sum(item.precio_total for item in queryset)
                    
            except LookupError:
                # El modelo no existe en esa app (ej: spa aún no instalado)
                continue
            except AttributeError:
                # La relación no existe o el campo precio_total no está
                continue
            except Exception:
                # Cualquier otro error
                continue
        
        return total


class ReservaServicio(BaseAuditModel):
    """
    Clase abstracta para cualquier servicio reservable.
    """
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        #Asociacion de abstraccion que se define en cada clase
        null=True,
        blank=True
    )
    
    tarifa_aplicada = models.ForeignKey(
        'finance.Tarifa',
        on_delete=models.PROTECT,
        null=True,
        editable=False
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

    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        editable=False,
        default=0
        )
    descuento = models.DecimalField( #Por ahora es manual se planea hacer lo mismo que con Recargo
        max_digits=10, 
        decimal_places=2, 
        default=0
        )
    """
    Futura implimentación de logica de negocio, debido que necesita su propia logica de negocio
    recargo = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=0
        )
    """
    precio_total = models.DecimalField(
        max_digits=12,
        decimal_places=2, 
        editable=False,
        default=0
        )

    observaciones = models.TextField(blank=True)
    
    class Meta:
        abstract = True
    
    def get_tarifa_vigente(self):
        raise NotImplementedError
    
    def calcular_precio(self):
        raise NotImplementedError
    
    def save(self, *args, **kwargs):
        self.calcular_precio()
        super().save(*args, **kwargs)