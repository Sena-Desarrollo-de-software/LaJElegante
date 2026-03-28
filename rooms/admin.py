from django.contrib import admin
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET, ReservaServicioInline, ReservaAdmin
from .models import TipoHabitacion, Habitacion, ReservaHabitacion

# === FUNCIONES AUXILIARES ===
def formatear_precio(precio):
    if not precio:
        return "Pendiente"
    return f"${precio:,.2f}".replace(',', '.')

def get_precio_total_formateado(obj):
    return formatear_precio(obj.precio_total)
get_precio_total_formateado.short_description = 'Total'

# === INLINES ===
class ReservaHabitacionServicioInline(ReservaServicioInline):
    """Inline para agregar reservas de habitación desde ReservaAdmin"""
    model = ReservaHabitacion
    fields = ('get_habitacion_info', 'fecha_inicio', 'fecha_fin', 'cantidad_personas', 'estado', 'get_precio_total')
    readonly_fields = ('get_habitacion_info', 'get_precio_total')
    
    def get_habitacion_info(self, obj):
        return f"{obj.habitacion} - {obj.habitacion.tipo_habitacion}"
    get_habitacion_info.short_description = 'Habitación'
    
    def get_precio_total(self, obj):
        return formatear_precio(obj.precio_total)
    get_precio_total.short_description = 'Total'

# Agregar inline a ReservaAdmin
ReservaAdmin.inlines.append(ReservaHabitacionServicioInline)

# === ADMINISTRADORES ===
@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre_tipo', 'capacidad_maxima', 'is_active')
    list_filter = ('nombre_tipo', 'is_active')
    search_fields = ('nombre_tipo',)
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Información del Tipo', {
            'fields': ('nombre_tipo', 'descripcion', 'capacidad_maxima')
        }),
        AUDITORIA_FIELDSET,
    )


@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = ('numero_habitacion', 'tipo_habitacion', 'estado', 'is_active')
    list_filter = ('tipo_habitacion', 'estado', 'is_active')
    search_fields = ('numero_habitacion',)
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Información de la Habitación', {
            'fields': ('numero_habitacion', 'tipo_habitacion', 'estado')
        }),
        AUDITORIA_FIELDSET,
    )
    
    actions = ['disponibles', 'mantenimiento']
    
    def disponibles(self, request, queryset):
        updated = queryset.update(estado='DISPONIBLE')
        self.message_user(request, f"{updated} habitaciones marcadas como disponibles.")
    disponibles.short_description = 'Marcar como disponibles'
    
    def mantenimiento(self, request, queryset):
        updated = queryset.update(estado='MANTENIMIENTO')
        self.message_user(request, f"{updated} habitaciones marcadas en mantenimiento.")
    mantenimiento.short_description = 'Marcar en mantenimiento'


@admin.register(ReservaHabitacion)
class ReservaHabitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_cliente',
        'get_habitacion',
        'fecha_inicio',
        'fecha_fin',
        'cantidad_noches',
        'cantidad_personas',
        'estado',
        'get_total',
        'is_active'
    )
    
    search_fields = ('reserva__usuario__username', 'reserva__usuario__email', 'habitacion__numero_habitacion')
    list_filter = ('estado', 'habitacion__tipo_habitacion', 'fecha_inicio', 'is_active')
    date_hierarchy = 'fecha_inicio'
    readonly_fields = AUDITORIA_READONLY + ('precio_unitario', 'precio_total', 'cantidad_noches')
    
    fieldsets = (
        ('Cliente', {
            'fields': ('reserva',)
        }),
        ('Detalles de la Reserva', {
            'fields': ('habitacion', 'fecha_inicio', 'fecha_fin', 'cantidad_personas', 'estado', 'observaciones')
        }),
        ('Precios', {
            'fields': ('descuento', 'precio_unitario', 'precio_total', 'cantidad_noches'),
            'classes': ('collapse',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    def get_cliente(self, obj):
        if obj.reserva and obj.reserva.usuario:
            return obj.reserva.usuario.get_full_name() or obj.reserva.usuario.username
        return "Cliente por definir"
    get_cliente.short_description = 'Cliente'
    
    def get_habitacion(self, obj):
        return f"{obj.habitacion.numero_habitacion} - {obj.habitacion.tipo_habitacion}"
    get_habitacion.short_description = 'Habitación'
    
    def get_total(self, obj):
        return formatear_precio(obj.precio_total)
    get_total.short_description = 'Total'
    
    def save_model(self, request, obj, form, change):
        """Si no tiene reserva, crear una automáticamente"""
        if not obj.reserva_id:
            from core.models import Reserva
            obj.reserva = Reserva.objects.create(
                usuario=request.user,
                estado=obj.estado
            )
        super().save_model(request, obj, form, change)
    
    actions = ['confirmar_reservas', 'cancelar_reservas', 'completar_reservas']
    
    def confirmar_reservas(self, request, queryset):
        for reserva in queryset:
            if hasattr(reserva, 'confirmar'):
                reserva.confirmar()
            else:
                reserva.estado = 'CONFIRMADA'
                reserva.save()
        self.message_user(request, f"{queryset.count()} reservas confirmadas.")
    
    def cancelar_reservas(self, request, queryset):
        for reserva in queryset:
            if hasattr(reserva, 'cancelar'):
                reserva.cancelar()
            else:
                reserva.estado = 'CANCELADA'
                reserva.save()
        self.message_user(request, f"{queryset.count()} reservas canceladas.")
    
    def completar_reservas(self, request, queryset):
        for reserva in queryset:
            if hasattr(reserva, 'completar'):
                reserva.completar()
            else:
                reserva.estado = 'COMPLETADA'
                reserva.save()
        self.message_user(request, f"{queryset.count()} reservas completadas.")