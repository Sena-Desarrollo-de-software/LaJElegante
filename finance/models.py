from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from core.models import BaseAuditModel
from django.db import models
from decimal import Decimal


# === IMPUESTO ===
class Impuesto(BaseAuditModel):
    """
    Catálogo de impuestos aplicables en el hotel.
    Basado en normativa Bogotá D.C.
    """
    TIPO_IMPUESTO_CHOICES = [
        ('IVA', 'IVA (19%)'),
        ('ICA', 'ICA (Industria y Comercio)'),
        ('TIMBRE', 'Impuesto de Timbre (1.5%)'),
        ('PROPINA', 'Propina (voluntaria)'),
        ('CONSUMO', 'Impuesto al Consumo'),
    ]
    
    APLICA_A_CHOICES = [
        ('HABITACION', 'Solo habitación'),
        ('RESTAURANTE', 'Solo restaurante'),
        ('SERVICIOS', 'Servicios adicionales'),
        ('TODOS', 'Todos los servicios'),
    ]
    
    nombre = models.CharField(
        max_length=100,
        verbose_name="nombre del impuesto"
    )
    
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_IMPUESTO_CHOICES,
        verbose_name="tipo de impuesto"
    )
    
    porcentaje = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="porcentaje (%)"
    )
    
    aplica_a = models.CharField(
        max_length=20,
        choices=APLICA_A_CHOICES,
        default='TODOS',
        verbose_name="aplica a"
    )
    
    es_obligatorio = models.BooleanField(
        default=True,
        verbose_name="es obligatorio"
    )
    
    aplica_extranjeros = models.BooleanField(
        default=True,
        verbose_name="aplica a extranjeros"
    )
    
    requiere_informacion_adicional = models.BooleanField(
        default=False,
        verbose_name="requiere texto informativo"
    )
    
    texto_informativo = models.TextField(
        blank=True,
        verbose_name="texto informativo",
        help_text="Ej: Texto obligatorio para propina según Circular 2 de 2012"
    )
    
    fecha_vigencia_inicio = models.DateField(
        verbose_name="fecha de inicio de vigencia"
    )
    
    fecha_vigencia_fin = models.DateField(
        null=True,
        blank=True,
        verbose_name="fecha de fin de vigencia"
    )
    
    class Meta:
        verbose_name = "impuesto"
        verbose_name_plural = "impuestos"
        ordering = ['tipo', 'fecha_vigencia_inicio']
        indexes = [
            models.Index(fields=['tipo', 'fecha_vigencia_inicio']),
        ]
    
    def __str__(self):
        vigencia = f"({self.fecha_vigencia_inicio}"
        if self.fecha_vigencia_fin:
            vigencia += f" - {self.fecha_vigencia_fin}"
        vigencia += ")"
        return f"{self.get_tipo_display()} - {self.porcentaje}% {vigencia}"
        # Ejemplo formato: "IVA - 19% (2025-01-01 - 2025-12-31)"
    
    def clean(self):
        if self.fecha_vigencia_fin and self.fecha_vigencia_inicio > self.fecha_vigencia_fin:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin")


# === TEMPORADA ===
class Temporada(BaseAuditModel):
    #Temporadas del hotel que afectan precios.
    class Nombre(models.TextChoices):
        ALTA = 'ALTA', 'Alta'
        MEDIA = 'MEDIA', 'Media'
        BAJA = 'BAJA', 'Baja'

    nombre = models.CharField(
        max_length=50,
        choices=Nombre.choices,
        verbose_name="nombre de temporada"
    )
    
    fecha_inicio = models.DateField(
        verbose_name="fecha de inicio"
    )
    
    fecha_fin = models.DateField(
        verbose_name="fecha de fin"
    )
    
    porcentaje_modificador = models.IntegerField(
        default=0,
        help_text="Ej: 20 para +20%, -10 para -10%",
        verbose_name="ajuste de precio (%)"
    )
    
    modificador_precio = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        editable=False,
        verbose_name="modificador (decimal)"
    )

    class Meta:
        verbose_name = "temporada"
        verbose_name_plural = "temporadas"
        ordering = ['fecha_inicio']
        unique_together = ['nombre', 'fecha_inicio', 'fecha_fin'] 

    def __str__(self):
        return f"{self.get_nombre_display()} ({self.fecha_inicio} - {self.fecha_fin})"

    def clean(self):
        if self.fecha_inicio >= self.fecha_fin:
            raise ValidationError("La fecha de inicio debe ser anterior a la fecha de fin")
    def save(self, *args, **kwargs):
        # Convertir porcentaje a decimal ANTES de guardar
        self.modificador_precio = 1 + (Decimal(str(self.porcentaje_modificador)) / 100)
        super().save(*args, **kwargs)
    
    def get_signo_porcentaje(self):
        # Devuelve el porcentaje con signo para mostrar en templates
        signo = "+" if self.porcentaje_modificador > 0 else ""
        return f"{signo}{self.porcentaje_modificador}%"


# === RELACIÓN TARIFA-IMPUESTO ===
class TarifaImpuesto(models.Model):
    # Tabla intermedia para asignar impuestos específicos a tarifas.
    tarifa = models.ForeignKey(
        'Tarifa',
        on_delete=models.CASCADE,
        verbose_name="tarifa"
    )
    
    impuesto = models.ForeignKey(
        Impuesto,
        on_delete=models.CASCADE,
        verbose_name="impuesto"
    )
    
    is_active = models.BooleanField(
        default=True,
    )
    
    class Meta:
        verbose_name = "impuesto de tarifa"
        verbose_name_plural = "impuestos de tarifa"
        unique_together = ['tarifa', 'impuesto']

    def __str__(self):
        return f"{self.tarifa} - {self.impuesto}"


# === TARIFA ===
class Tarifa(BaseAuditModel):
    # Tarifas por tipo de habitación y temporada.
    class Estado(models.TextChoices):
        VIGENTE = 'VIGENTE', 'Vigente'
        INACTIVA = 'INACTIVA', 'Inactiva'

    estado = models.CharField(
        max_length=10,
        choices=Estado.choices,
        default=Estado.VIGENTE,
        verbose_name="estado"
    )
    #Relacion polimorfica de llaves foraneas
    servicio_tipo = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    
    servicio_id = models.PositiveIntegerField()

    servicio = GenericForeignKey('servicio_tipo','servicio_id')
    
    temporada = models.ForeignKey(
        Temporada,
        on_delete=models.PROTECT,
        related_name='tarifas',
        db_column='id_temporada',
        verbose_name="temporada"
    )

    precio_base = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="precio base (sin impuestos)"
    )

    precio_final = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        verbose_name="precio final (con impuestos)"
    )

    impuestos = models.ManyToManyField(
        Impuesto,
        through=TarifaImpuesto,
        related_name='tarifas_aplicadas',
        blank=True,
        verbose_name="impuestos aplicables"
    )

    class Meta:
        verbose_name = 'tarifa'
        verbose_name_plural = 'tarifas'
    
    def calcular_precio_final(self, es_extranjero=False):
        precio, _ = self._calcular_precios(es_extranjero)
        return precio

    def get_desglose_impuestos(self, es_extranjero=False):
        _, desglose = self._calcular_precios(es_extranjero)
        return desglose

    def _calcular_precios(self, es_extranjero=False, impuestos_ids=None):
        from django.utils import timezone
        
        precio = self.precio_base or Decimal('0.00')
        desglose = {}
        
        # Aplicar modificador de temporada
        if self.temporada_id:
            precio = precio * self.temporada.modificador_precio
        
        # Obtener IDs de impuestos (pasados como parámetro o desde la instancia)
        if impuestos_ids is None and self.pk:
            # Si ya existe en BD, usar relación
            impuestos_qs = self.impuestos.filter(
                is_active=True,
                fecha_vigencia_inicio__lte=timezone.now().date()
            ).filter(
                models.Q(fecha_vigencia_fin__isnull=True) |
                models.Q(fecha_vigencia_fin__gte=timezone.now().date())
            )
        else:
            # Si es nuevo, usar IDs proporcionados
            impuestos_qs = Impuesto.objects.filter(
                id__in=impuestos_ids or [],
                is_active=True,
                fecha_vigencia_inicio__lte=timezone.now().date()
            ).filter(
                models.Q(fecha_vigencia_fin__isnull=True) |
                models.Q(fecha_vigencia_fin__gte=timezone.now().date())
            )
        
        # Aplicar impuestos
        for impuesto in impuestos_qs:
            if es_extranjero and not impuesto.aplica_extranjeros:
                continue
            
            if impuesto.aplica_a not in ['TODOS', 'HABITACION']:
                continue
            
            valor_impuesto = precio * (impuesto.porcentaje / 100)
            desglose[impuesto.tipo] = {
                'nombre': impuesto.nombre,
                'porcentaje': impuesto.porcentaje,
                'valor': valor_impuesto,
            }
            precio += valor_impuesto
        
        return precio, desglose

    def save(self, *args, **kwargs):
        if not self.pk:
            impuestos_ids = kwargs.pop('impuestos_ids', None)
            self.precio_final, _ = self._calcular_precios(
                es_extranjero=False, 
                impuestos_ids=impuestos_ids
            )
        else:
            self.precio_final, _ = self._calcular_precios(es_extranjero=False)
        
        super().save(*args, **kwargs)

# Metodo helper
def get_tarifa_vigente(servicio_tipo,servicio_id, fecha):
    # Obtiene la tarifa vigente para un tipo de habitación en una fecha específica.
    return Tarifa.objects.filter(
        servicio_tipo=servicio_tipo,
        servicio_id=servicio_id,
        estado='VIGENTE',
        temporada__fecha_inicio__lte=fecha,
        temporada__fecha_fin__gte=fecha
    ).select_related('temporada').first()