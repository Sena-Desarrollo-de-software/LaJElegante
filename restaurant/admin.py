from django.contrib import admin
from .models import Horario, Turno, ReservaRestaurante
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET, AUDITORIA_LIST_DISPLAY, ReservaServicioInline, ReservaAdmin

# === FUNCIONES AUXILIARES ===
def formatear_precio(precio):
    if not precio:
        return "Pendiente"
    return f"${precio:,.2f}".replace(',', '.')

# === INLINES ===
class ReservaRestauranteInline(admin.TabularInline):
    """Muestra las reservas dentro del turno"""
    model = ReservaRestaurante
    extra = 0
    fields = (
        'get_cliente',
        'cantidad',
        'estado',
        'get_total'
    )
    readonly_fields = fields
    
    def get_cliente(self, obj):
        return obj.reserva.usuario.get_full_name() or obj.reserva.usuario.username
    get_cliente.short_description = 'Cliente'
    
    def get_total(self, obj):
        return formatear_precio(obj.precio_total)
    get_total.short_description = 'Total'
    
    def has_add_permission(self, request, obj=None):
        return False

class ReservaRestauranteServicioInline(ReservaServicioInline):
    """Inline para agregar servicios de restaurante desde ReservaAdmin"""
    model = ReservaRestaurante
    # Puedes personalizar los campos si quieres
    fields = ('turno', 'cantidad', 'estado', 'get_precio_total')
    readonly_fields = ('get_precio_total',)

ReservaAdmin.inlines.append(ReservaRestauranteServicioInline)
# === ADMINISTRADORES ===
@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = (
        'turno',
        'hora_inicio',
        'hora_fin',
        'capacidad_maxima',
        'is_active'
    )
    list_filter = ('turno', 'is_active')
    search_fields = ('turno',)
    readonly_fields = AUDITORIA_READONLY
    
    fieldsets = (
        ('Información del Horario', {
            'fields': ('turno', 'hora_inicio', 'hora_fin', 'capacidad_maxima')
        }),
        AUDITORIA_FIELDSET,
    )


@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    list_display = (
        'horario',
        'fecha',
        'quorum',
        'capacidad_efectiva',
        'capacidad_disponible',
        'is_active'
        )
    list_filter = ('horario', 'fecha', 'is_active')
    search_fields = ('fecha', 'horario__turno')
    readonly_fields = AUDITORIA_READONLY + ('quorum', 'capacidad_disponible', 'capacidad_efectiva')
    
    fieldsets = (
        ('Información del Turno', {
            'fields': ('horario', 'fecha')
        }),
        ('Capacidad', {
            'fields': ('capacidad_maxima',),
            'description': 'Dejar vacío para usar la capacidad del horario',
            'classes': ('collapse',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    inlines = [ReservaRestauranteInline]
    
    def capacidad_efectiva(self, obj):
        return obj.capacidad_maxima or obj.horario.capacidad_maxima
    capacidad_efectiva.short_description = 'Capacidad máxima'
    
    def capacidad_disponible(self, obj):
        efectiva = obj.capacidad_maxima or obj.horario.capacidad_maxima
        return efectiva - obj.quorum
    capacidad_disponible.short_description = 'Lugares libres'


@admin.register(ReservaRestaurante)
class ReservaRestauranteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_cliente',
        'get_turno',
        'cantidad',
        'estado',
        'get_total',
        'is_active'
    )
    
    search_fields = ('reserva__usuario__username', 'reserva__usuario__email', 'turno__fecha')
    list_filter = ('estado', 'turno__horario', 'is_active')
    readonly_fields = AUDITORIA_READONLY + ('precio_unitario', 'precio_total')
    
    fieldsets = (
        ('Cliente', {
            'fields': ('reserva',)
        }),
        ('Reserva', {
            'fields': ('turno', 'cantidad', 'estado', 'observaciones')
        }),
        ('Precios', {
            'fields': ('descuento', 'precio_unitario', 'precio_total'),
            'classes': ('collapse',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    def get_cliente(self, obj):
        return obj.reserva.usuario.get_full_name() or obj.reserva.usuario.username
    get_cliente.short_description = 'Cliente'
    
    def get_turno(self, obj):
        return f"{obj.turno.horario} - {obj.turno.fecha}"
    get_turno.short_description = 'Turno'
    
    def get_total(self, obj):
        return formatear_precio(obj.precio_total)
    get_total.short_description = 'Total'
    
    actions = ['confirmar_reservas', 'cancelar_reservas']
    
    def confirmar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.confirmar()
        self.message_user(request, f"{queryset.count()} reservas confirmadas.")

    def cancelar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.cancelar()
        self.message_user(request, f"{queryset.count()} reservas canceladas.")

    def completar_reservas(self, request, queryset):
        for reserva in queryset:
            reserva.completar()
        self.message_user(request, f"{queryset.count()} reservas completadas.")