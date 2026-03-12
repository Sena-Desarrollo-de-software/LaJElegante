from django.contrib import admin
from django.utils import timezone
from .models import TipoHabitacion, Habitacion, DetallesReservaHabitacion, ReservaHabitacion
from core.admin import AUDITORIA_FIELDSET,AUDITORIA_READONLY

@admin.register(TipoHabitacion)
class TipoHabitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_tipo',
        'get_nombre_tipo_display',
        'capacidad_maxima',
        'total_habitaciones',
        'is_active',
        'created_at',
        'updated_at'
    )
    
    search_fields = ('nombre_tipo', 'descripcion')
    
    list_filter = (
        'nombre_tipo',
        'capacidad_maxima',
        'is_active',
        'created_at'
    )
    
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Información del Tipo', {
            'fields': ('nombre_tipo', 'descripcion', 'capacidad_maxima')
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('nombre_tipo', 'descripcion', 'capacidad_maxima', 'is_active')
        }),
    )
    
    def total_habitaciones(self, obj):
        return obj.habitaciones.count()
    total_habitaciones.short_description = 'Total Habitaciones'
    
    actions = ['activar_tipos', 'desactivar_tipos']
    
    def activar_tipos(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} tipos activados.")
    activar_tipos.short_description = "Activar tipos seleccionados"
    
    def desactivar_tipos(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} tipos desactivados.")
    desactivar_tipos.short_description = "Desactivar tipos seleccionados"

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_habitacion',
        'tipo_habitacion',
        'get_tipo_nombre',
        'estado_habitacion',
        'get_estado_habitacion_display',
        'reservas_activas',
        'is_active',
        'created_at'
    )
    
    search_fields = ('numero_habitacion', 'tipo_habitacion__nombre_tipo')
    
    list_filter = (
        'estado_habitacion',
        'tipo_habitacion',
        'is_active',
        'created_at'
    )
    
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Información de Habitación', {
            'fields': ('numero_habitacion', 'tipo_habitacion', 'estado_habitacion')
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_habitacion', 'tipo_habitacion', 'estado_habitacion', 'is_active')
        }),
    )
    
    def get_tipo_nombre(self, obj):
        return obj.tipo_habitacion.get_nombre_tipo_display()
    get_tipo_nombre.short_description = 'Tipo'
    
    def reservas_activas(self, obj):
        return obj.detalles_reserva.filter(reserva_habitacion__isnull=False, is_active=True).count()
    reservas_activas.short_description = 'Reservas Activas'
    
    actions = ['marcar_mantenimiento', 'marcar_servicio', 'marcar_eliminado']
    
    def marcar_mantenimiento(self, request, queryset):
        updated = queryset.update(estado_habitacion='MANTENIMIENTO')
        self.message_user(request, f"{updated} habitaciones en mantenimiento.")
    marcar_mantenimiento.short_description = "Marcar como mantenimiento"
    
    def marcar_servicio(self, request, queryset):
        updated = queryset.update(estado_habitacion='EN_SERVICIO')
        self.message_user(request, f"{updated} habitaciones en servicio.")
    marcar_servicio.short_description = "Marcar como en servicio"
    
    def marcar_eliminado(self, request, queryset):
        updated = queryset.update(deleted_at=timezone.now(), is_active=False)
        self.message_user(request, f"{updated} habitaciones eliminadas.")
    marcar_eliminado.short_description = "Marcar como eliminadas"

class DetallesReservaInline(admin.TabularInline):
    model = DetallesReservaHabitacion
    extra = 1
    fields = (
        'habitacion', 
        'fecha_inicio', 
        'fecha_fin', 
        'cantidad_personas', 
        'cantidad_noches',
        'precio_por_noche',
        'precio_total'
    )
    readonly_fields = ('cantidad_noches', 'precio_por_noche', 'precio_total')

@admin.register(ReservaHabitacion)
class ReservaHabitacionAdmin(admin.ModelAdmin):
    inlines = [DetallesReservaInline]
    
    list_display = (
        'id',
        'usuario',
        'get_cliente_nombre',
        'total_habitaciones',
        'precio_total',
        'is_active',
        'created_at'
    )
    
    search_fields = ('usuario__username', 'usuario__email')
    
    list_filter = (
        'created_at',
        'is_active',
        'detalles__habitacion__tipo_habitacion'
    )
    
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Cliente', {
            'fields': ('usuario',)
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    def get_cliente_nombre(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.username
    get_cliente_nombre.short_description = 'Cliente'
    
    def total_habitaciones(self, obj):
        return obj.detalles.count()
    total_habitaciones.short_description = 'Habitaciones'
    
    def precio_total(self, obj):
        return sum(detalle.precio_reserva for detalle in obj.detalles.all())
    precio_total.short_description = 'Total'
    
    actions = ['marcar_eliminado']
    
    def marcar_eliminado(self, request, queryset):
        updated = queryset.update(deleted_at=timezone.now(), is_active=False)
        for reserva in queryset:
            reserva.detalles.all().update(is_active=False)
        self.message_user(request, f"{updated} reservas eliminadas.")
    marcar_eliminado.short_description = "Marcar como eliminadas"

@admin.register(DetallesReservaHabitacion)
class DetallesReservaHabitacionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_reserva_id',
        'get_cliente',
        'habitacion',
        'fecha_inicio',
        'fecha_fin',
        'cantidad_personas',
        'precio_total',
        'is_active'
    )
    
    list_filter = (
        'habitacion__tipo_habitacion',
        'fecha_inicio',
        'cantidad_personas',
        'is_active'
    )
    
    search_fields = (
        'reserva__usuario__username',
        'reserva__usuario__email',
        'habitacion__numero_habitacion'
    )
    
    date_hierarchy = 'fecha_inicio'
    
    readonly_fields = AUDITORIA_READONLY + ('precio_total',)
    
    fieldsets = (
        ('Información de Reserva', {
            'fields': ('reserva', 'habitacion')
        }),
        ('Detalles de Estadía', {
            'fields': ('fecha_inicio', 'fecha_fin', 'cantidad_personas', 'cantidad_noches')
        }),
        ('Precios', {
            'fields': ('precio_noche', 'descuento_aplicado', 'recargo_aplicado', 'precio_reserva')
        }),
        ('Observaciones', {
            'fields': ('observacion',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    def get_reserva_id(self, obj):
        return obj.reserva.id
    get_reserva_id.short_description = 'Reserva #'
    
    def get_cliente(self, obj):
        return obj.reserva.usuario.username
    get_cliente.short_description = 'Cliente'
