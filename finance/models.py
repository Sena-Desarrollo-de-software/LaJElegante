from django.db import models
from django.core.exceptions import ValidationError
from rooms.models import TipoHabitacion
from core.models import BaseAuditModel
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
    
    activo = models.BooleanField(
        default=True,
        verbose_name="activo"
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

    tipo_habitacion = models.ForeignKey(
        TipoHabitacion,
        on_delete=models.CASCADE,
        related_name='tarifas',
        db_column='id_tipo_habitacion',
        verbose_name="tipo de habitación"
    )
    
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
        verbose_name = "tarifa"
        verbose_name_plural = "tarifas"
        unique_together = ['tipo_habitacion', 'temporada']
        indexes = [
            models.Index(fields=['estado', 'tipo_habitacion', 'temporada']),
        ]

    def __str__(self):
        return f"{self.tipo_habitacion} - {self.temporada} - ${self.precio_base}"
    
    def _calcular_precios(self, es_extranjero=False):
        from django.utils import timezone
        
        precio = self.precio_base
        desglose = {}
        
        # Aplicar modificador de temporada
        if self.temporada and abs(self.temporada.modificador_precio - Decimal('1.0')) > Decimal('0.000001'):
            precio = precio * self.temporada.modificador_precio
        
        # Obtener impuestos aplicables
        impuestos_aplicables = self.impuestos.filter(
            activo=True,
            fecha_vigencia_inicio__lte=timezone.now().date()
        ).filter(
            models.Q(fecha_vigencia_fin__isnull=True) |
            models.Q(fecha_vigencia_fin__gte=timezone.now().date())
        )
        # Q para realizar consultar con OR
        # Aplicar impuestos
        for impuesto in impuestos_aplicables:
            if es_extranjero and not impuesto.aplica_extranjeros:
                continue
            
            if impuesto.aplica_a not in ['TODOS', 'HABITACION']:
                continue
            
            valor_impuesto = precio * (impuesto.porcentaje / 100)
            desglose[impuesto.tipo] = {
                'nombre': impuesto.nombre,
                'porcentaje': impuesto.porcentaje,
                'valor': valor_impuesto,
                'texto_info': impuesto.texto_informativo if impuesto.requiere_informacion_adicional else None
            }
            precio += valor_impuesto
        
        return precio, desglose

    def calcular_precio_final(self, es_extranjero=False):

        precio, _ = self._calcular_precios(es_extranjero)
        return precio

    def get_desglose_impuestos(self, es_extranjero=False):
        _, desglose = self._calcular_precios(es_extranjero)
        return desglose

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

        self.precio_final, _ = self._calcular_precios(es_extranjero=False)
        
        super().save(update_fields=['precio_final'])

# Metodo helper
def obtener_tarifa_vigente(tipo_habitacion_id, fecha):
    # Obtiene la tarifa vigente para un tipo de habitación en una fecha específica.
    return Tarifa.objects.filter(
        tipo_habitacion_id=tipo_habitacion_id,
        estado='VIGENTE',
        temporada__fecha_inicio__lte=fecha,
        temporada__fecha_fin__gte=fecha
    ).select_related('temporada').first()