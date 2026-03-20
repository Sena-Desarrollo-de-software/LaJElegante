from django.db import models
from core.models import BaseAuditModel
from core.models import ReservaServicio


# === DÍA DE LA SEMANA ===
class DiaSemana(models.Model):
    """Catálogo de días de la semana"""
    numero = models.PositiveSmallIntegerField(unique=True)  # 1-7
    nombre = models.CharField(max_length=10)
    nombre_corto = models.CharField(max_length=3)  # Lun, Mar, etc.
    
    class Meta:
        verbose_name = "día de la semana"
        verbose_name_plural = "días de la semana"
        ordering = ['numero']
    
    def __str__(self):
        return self.nombre

# === HORARIO DE SERVICIO ===
class HorarioServicio(BaseAuditModel):
    """
    Define los diferentes momentos del día para servicio de alimentos
    """
    TIPO_SERVICIO_CHOICES = [
        ('DESAYUNO', 'Desayuno'),
        ('ALMUERZO', 'Almuerzo'),
        ('CENA', 'Cena'),
        ('BAR', 'Bar / Room Service'),
        ('BRUNCH', 'Brunch'),
        ('OTRO', 'Otro horario'),
    ]
    
    nombre = models.CharField(
        max_length=20,
        choices=TIPO_SERVICIO_CHOICES,
        unique=True
    )
    
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    
    dias_disponibles = models.ManyToManyField(
        DiaSemana,
        related_name="horarios",
        verbose_name="días disponibles"
    )
    
    requiere_reserva_previa = models.BooleanField(default=True)
    horas_anticipacion = models.PositiveIntegerField(default=0)
    
    class Meta:
        verbose_name = "horario de servicio"
        verbose_name_plural = "horarios de servicio"
        ordering = ['hora_inicio']
    
    def __str__(self):
        return f"{self.get_nombre_display()} ({self.hora_inicio} - {self.hora_fin})"
    
    def esta_disponible(self, fecha, hora):
        """Verifica si el horario está disponible para una fecha/hora"""
        dia_semana = fecha.isoweekday()
        
        if dia_semana not in self.dias_semana:
            return False
        
        if not (self.hora_inicio <= hora <= self.hora_fin):
            return False
        
        return True


# === CATEGORÍA DE MENÚ ===
class CategoriaMenu(BaseAuditModel):
    """
    Ej: Entradas, Platos fuertes, Postres, Bebidas, Buffet
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveIntegerField(default=0)
    
    # Para identificar categorías especiales
    es_buffet = models.BooleanField(default=False)
    requiere_preparacion = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "categoría de menú"
        verbose_name_plural = "categorías de menú"
        ordering = ['orden']
    
    def __str__(self):
        return self.nombre


# === ITEM DE MENÚ ===
class ItemMenu(BaseAuditModel):
    """
    Cada plato, bebida o servicio que se puede ofrecer
    """
    categoria = models.ForeignKey(
        CategoriaMenu,
        on_delete=models.PROTECT,
        related_name="items"
    )
    
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    
    # Control de disponibilidad
    disponible = models.BooleanField(default=True)
    horarios_disponibles = models.ManyToManyField(
        HorarioServicio,
        blank=True,
        related_name="items_disponibles"
    )
    
    # Tiempo estimado de preparación (minutos)
    tiempo_preparacion = models.PositiveIntegerField(default=15)
    
    # Para control de inventario (opcional)
    control_stock = models.BooleanField(default=False)
    stock_actual = models.PositiveIntegerField(default=0, blank=True)
    
    class Meta:
        verbose_name = "ítem de menú"
        verbose_name_plural = "ítems de menú"
        unique_together = ['categoria', 'nombre']
        indexes = [
            models.Index(fields=['disponible', 'categoria']),
        ]
    
    def __str__(self):
        return f"{self.categoria.nombre} - {self.nombre}"


# === MENÚ EJECUTIVO (COMBOS) ===
class MenuEjecutivo(BaseAuditModel):
    """
    Combinaciones de items (ej: Almuerzo ejecutivo: entrada + plato + postre)
    """
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    
    items = models.ManyToManyField(
        ItemMenu,
        through='MenuEjecutivoItem',
        related_name="menus_ejecutivos"
    )
    
    horarios_disponibles = models.ManyToManyField(
        HorarioServicio,
        related_name="menus_ejecutivos"
    )
    
    precio_especial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Si es nulo, se suma precio de items"
    )
    
    class Meta:
        verbose_name = "menú ejecutivo"
        verbose_name_plural = "menús ejecutivos"
    
    def __str__(self):
        return self.nombre


# === ITEMS DE MENÚ EJECUTIVO ===
class MenuEjecutivoItem(models.Model):
    """Tabla intermedia para ordenar items dentro del menú"""
    menu_ejecutivo = models.ForeignKey(MenuEjecutivo, on_delete=models.CASCADE)
    item_menu = models.ForeignKey(ItemMenu, on_delete=models.CASCADE)
    orden = models.PositiveIntegerField(default=0)
    obligatorio = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['orden']
        unique_together = ['menu_ejecutivo', 'item_menu']


# === MESA ===
class Mesa(BaseAuditModel):
    numero_mesa = models.SmallIntegerField()
    capacidad = models.SmallIntegerField()
    zona = models.CharField(max_length=50)
    ubicacion_detalle = models.CharField(max_length=150)
    
    # Para control de reservas
    tiempo_entre_reservas = models.PositiveIntegerField(
        default=30,
        help_text="Minutos necesarios entre reservas"
    )
    
    class Meta:
        verbose_name = "mesa"
        verbose_name_plural = "mesas"
        ordering = ['zona', 'numero_mesa']
        unique_together = ['numero_mesa', 'zona']
    
    def __str__(self):
        return f"Mesa {self.numero_mesa} - {self.zona} ({self.capacidad} pers.)"
    
    def disponible_en_horario(self, fecha, hora_inicio, hora_fin):
        """Verifica disponibilidad de la mesa en un rango horario"""
        from django.db.models import Q
        
        # Buscar reservas que se solapen
        reservas = ReservaRestaurante.objects.filter(
            mesa=self,
            fecha_reserva=fecha,
            estado_reserva__in=['PENDIENTE', 'CONFIRMADA']
        ).filter(
            Q(hora_inicio__lt=hora_fin) & Q(hora_fin__gt=hora_inicio)
        )
        
        return not reservas.exists()


# === RESERVA RESTAURANTE (ahora hereda de ReservaServicio) ===
class ReservaRestaurante(ReservaServicio):
    """
    Reserva de restaurante que puede ser:
    - Reserva de mesa (buffet / servicio)
    - Pedido a la carta (múltiples items)
    - Menú ejecutivo
    """
    TIPO_RESERVA_CHOICES = [
        ('MESA', 'Solo reserva de mesa'),
        ('CARTA', 'Pedido a la carta'),
        ('EJECUTIVO', 'Menú ejecutivo'),
        ('BUFFET', 'Buffet libre'),
    ]
    
    # Relaciones principales
    mesa = models.ForeignKey(
        Mesa,
        on_delete=models.PROTECT,
        related_name="reservas"
    )
    
    horario_servicio = models.ForeignKey(
        HorarioServicio,
        on_delete=models.PROTECT,
        related_name="reservas"
    )
    
    tipo_reserva = models.CharField(
        max_length=20,
        choices=TIPO_RESERVA_CHOICES,
        default='MESA'
    )
    
    # Fecha y hora de la reserva
    fecha_reserva = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField(editable=False)  # Se calcula
    
    # Items seleccionados (para carta o ejecutivo)
    items = models.ManyToManyField(
        ItemMenu,
        through='ReservaRestauranteItem',
        blank=True,
        related_name="reservas"
    )
    
    menu_ejecutivo = models.ForeignKey(
        MenuEjecutivo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reservas"
    )
    
    # Control de personas
    numero_personas = models.PositiveIntegerField()
    
    # Estado específico (además del de ReservaServicio)
    ESTADO_RESERVA_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADA', 'Confirmada'),
        ('CANCELADA', 'Cancelada'),
        ('COMPLETADA', 'Completada'),
        ('NO_SHOW', 'No se presentó'),
    ]
    
    estado_restaurante = models.CharField(
        max_length=20,
        choices=ESTADO_RESERVA_CHOICES,
        default='PENDIENTE'
    )
    
    class Meta:
        verbose_name = "reserva de restaurante"
        verbose_name_plural = "reservas de restaurante"
        indexes = [
            models.Index(fields=['fecha_reserva', 'estado_restaurante']),
            models.Index(fields=['mesa', 'fecha_reserva', 'hora_inicio']),
        ]
    
    def __str__(self):
        return f"Reserva Rest #{self.id} - {self.fecha_reserva} {self.hora_inicio}"
    
    def save(self, *args, **kwargs):
        # Calcular hora_fin basado en el tipo de servicio
        if self.horario_servicio and not self.hora_fin:
            # Duración estimada según tipo de servicio
            duracion = self._calcular_duracion()
            from datetime import datetime, timedelta
            hora_inicio_dt = datetime.combine(datetime.today(), self.hora_inicio)
            hora_fin_dt = hora_inicio_dt + timedelta(minutes=duracion)
            self.hora_fin = hora_fin_dt.time()
        
        super().save(*args, **kwargs)
    
    def _calcular_duracion(self):
        """Calcula duración estimada según tipo de servicio"""
        duraciones = {
            'DESAYUNO': 60,
            'ALMUERZO': 90,
            'CENA': 120,
            'BAR': 45,
        }
        return duraciones.get(self.horario_servicio.nombre, 90)
    
    def get_tarifa_vigente(self):
        """
        Obtiene tarifa según tipo de reserva
        """
        from finance.models import Tarifa
        from django.contrib.contenttypes.models import ContentType
        
        if self.tipo_reserva == 'BUFFET':
            # Tarifa por persona para buffet
            content_type = ContentType.objects.get_for_model(HorarioServicio)
            object_id = self.horario_servicio_id
        elif self.tipo_reserva == 'EJECUTIVO' and self.menu_ejecutivo:
            content_type = ContentType.objects.get_for_model(MenuEjecutivo)
            object_id = self.menu_ejecutivo_id
        else:
            # Para carta, se calcula por items (en otro método)
            return None
        
        return Tarifa.objects.filter(
            servicio_tipo=content_type,
            servicio_id=object_id,
            estado='VIGENTE'
        ).first()
    
    def calcular_precio(self):
        """Calcula el precio total de la reserva"""
        total = 0
        
        if self.tipo_reserva == 'BUFFET':
            tarifa = self.get_tarifa_vigente()
            if tarifa:
                total = tarifa.precio_final * self.numero_personas
        
        elif self.tipo_reserva == 'EJECUTIVO' and self.menu_ejecutivo:
            tarifa = self.get_tarifa_vigente()
            if tarifa:
                total = tarifa.precio_final * self.numero_personas
            else:
                # Sumar precios de items individuales
                for item_rel in self.reservarestauranteitem_set.all():
                    total += item_rel.subtotal
        
        # Guardar en campos heredados de ReservaServicio
        self.precio_total = total - self.descuento + self.recargo
        self.precio_unitario = total / self.numero_personas if self.numero_personas else 0


# === ITEMS DE RESERVA (para carta) ===
class ReservaRestauranteItem(models.Model):
    """Items seleccionados en una reserva a la carta"""
    reserva = models.ForeignKey(ReservaRestaurante, on_delete=models.CASCADE)
    item_menu = models.ForeignKey(ItemMenu, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)
    observaciones = models.CharField(max_length=200, blank=True)
    
    # Precio en el momento de la reserva
    precio_unitario_congelado = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        unique_together = ['reserva', 'item_menu']
    
    @property
    def subtotal(self):
        return self.precio_unitario_congelado * self.cantidad