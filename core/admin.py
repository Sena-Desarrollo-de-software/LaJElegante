from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from .models import Promocion

AUDITORIA_FIELDSET = ('Auditoría', {
    'fields': ('created_at', 'updated_at', 'deleted_at'),
    'classes': ('collapse',),
})

AUDITORIA_READONLY = ('created_at', 'updated_at', 'deleted_at')
        
AUDITORIA_LIST_DISPLAY ='is_active','created_at','updated_at'

@admin.register(Promocion)
class PromocionAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'tipo',
        'estado',
        'orden_navbar',
        'fecha_inicio',
        'fecha_fin',
        'estado_vigencia',
        'is_active'
    )
    
    list_filter = (
        'tipo',
        'estado',
        'is_active',
        'fecha_inicio',
        'fecha_fin'
    )
    
    search_fields = ('titulo', 'descripcion')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('titulo', 'descripcion', 'tipo', 'estado')
        }),
        ('Imágenes', {
            'fields': ('imagen_pequena', 'imagen_grande'),
        }),
        ('Configuración de Publicación', {
            'fields': ('fecha_inicio', 'fecha_fin', 'orden_navbar'),
        }),
        ('Estados del Sistema', {
            'fields': ('is_active',),
            'classes': ('collapse',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    readonly_fields = AUDITORIA_READONLY
    
    def estado_vigencia(self, obj):
        """Muestra si la promoción está activa según fechas"""
        ahora = timezone.now()
        
        if obj.estado != 'PUBLICADO':
            return "Borrador"
        
        if obj.fecha_inicio <= ahora <= obj.fecha_fin:
            return "Activa"
        elif ahora < obj.fecha_inicio:
            return "Programada"
        else:
            return "Expirada"
    estado_vigencia.short_description = 'Vigencia'
    
    actions = ['duplicar_promocion']
    
    def duplicar_promocion(self, request, queryset):
        """Duplica las promociones seleccionadas"""
        for promocion in queryset:
            promocion.pk = None
            promocion.titulo = f"{promocion.titulo} (copia)"
            promocion.estado = 'BORRADOR'
            promocion.orden_navbar = None
            promocion.save()
            
        self.message_user(
            request, 
            f"{queryset.count()} promoción(es) duplicada(s)."
        )
    duplicar_promocion.short_description = "Duplicar promociones seleccionadas"