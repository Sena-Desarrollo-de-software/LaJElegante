from django.db import models

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