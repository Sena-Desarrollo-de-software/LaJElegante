from django.contrib import admin
from django.utils import timezone
from .models import Promocion, Reserva

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

class ReservaServicioInline(admin.TabularInline):
    """Inline base para servicios - se extiende en cada app"""
    model = None  # Se define en las subclases
    extra = 0
    fields = ('get_servicio_info', 'cantidad', 'estado', 'get_precio_total')
    readonly_fields = fields
    
    def get_servicio_info(self, obj):
        return str(obj)
    get_servicio_info.short_description = 'Servicio'
    
    def get_precio_total(self, obj):
        if obj.precio_total:
            return f"${obj.precio_total:,.2f}".replace(',', '.')
        return "Pendiente"
    get_precio_total.short_description = 'Total'
    
    def has_add_permission(self, request, obj=None):
        return True

# Inline abstracto para servicios (se extiende en cada app)
@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'fecha_reserva',
        'estado',
        'total_reserva',
        'cantidad_servicios',
        'is_active'
    )
    
    list_filter = ('estado', 'is_active', 'fecha_reserva')
    search_fields = ('usuario__username', 'usuario__email', 'id')
    date_hierarchy = 'fecha_reserva'
    readonly_fields = AUDITORIA_READONLY + ('total_reserva',)
    
    fieldsets = (
        ('Información de la Reserva', {
            'fields': ('usuario', 'estado')
        }),
        ('Totales', {
            'fields': ('total_reserva',),
            'description': 'Total calculado automáticamente desde los servicios'
        }),
        AUDITORIA_FIELDSET,
    )

    inlines = []
    
    def total_reserva(self, obj):
        total = obj.total
        return f"${total:,.2f}".replace(',', '.') if total else "$0.00"
    total_reserva.short_description = 'Total'
    
    def cantidad_servicios(self, obj):
        # Contar todos los servicios relacionados
        count = 0
        # Esto se puede mejorar con un registro dinámico
        if hasattr(obj, 'reservarestaurantes'):
            count += obj.reservarestaurantes.count()
        return count
    cantidad_servicios.short_description = 'Servicios'
    
    actions = ['confirmar_reservas', 'cancelar_reservas', 'completar_reservas']
    
    def confirmar_reservas(self, request, queryset):
        updated = queryset.update(estado='CONFIRMADA')
        self.message_user(request, f"{updated} reservas confirmadas.")
    
    def cancelar_reservas(self, request, queryset):
        updated = queryset.update(estado='CANCELADA')
        self.message_user(request, f"{updated} reservas canceladas.")
    
    def completar_reservas(self, request, queryset):
        updated = queryset.update(estado='COMPLETADA')
        self.message_user(request, f"{updated} reservas completadas.")