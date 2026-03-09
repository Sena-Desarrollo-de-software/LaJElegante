from django.contrib import admin
from .models import Mesa,ReservaRestaurante
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET

@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'numero_mesa',
        'capacidad',
        'zona',
        'ubicacion_detalle',
        'total_reservas',
        'is_active',
        'created_at'
    )

    search_fields = ('numero_mesa', 'zona')

    list_filter = (
        'zona',
        'capacidad',
        'is_active',
        'created_at'
    )

    readonly_fields = AUDITORIA_READONLY

    fieldsets = (
        ('Información de Mesa', {
            'fields' : ('numero_mesa', 'capacidad', 'zona', 'ubicacion_detalle')
        }),
        ('Estados', {
            'fields' : ('is_active',)
        }),
        AUDITORIA_FIELDSET
    )

    def total_reservas(self, obj):
        return obj.reservas.count()
    total_reservas.short_description = 'Reservas'

@admin.register(ReservaRestaurante)
class ReservaRestauranteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'usuario',
        'get_cliente_nombre',
        'mesa',
        'fecha_reserva_corta',
        'hora_reserva',
        'numero_personas',
        'estado_reserva',
        'is_active'
    )

    search_fields = ('usuario__username', 'usuario__email', 'mesa__numero_mesa')

    list_filter = (
        'estado_reserva',
        'hora_reserva',
        'numero_personas',
        'is_active',
        'created_at'
    )

    date_hierarchy = 'created_at'

    readonly_fields = AUDITORIA_READONLY

    fieldsets = (
        ('Cliente', {
            'fields' : ('usuario',)
        }),
        ('Detalles de Reserva', {
            'fields' : ('mesa', 'hora_reserva', 'numero_personas')
        }),
        ('Estado', {
            'fields' : ('estado_reserva',)
        }),
        ('Estados', {
            'fields' : ('is_active',)
        }),
        AUDITORIA_FIELDSET
    )

    def get_cliente_nombre(self, obj):
        return f"{obj.usuario.first_name} {obj.usuario.last_name}".strip() or obj.usuario.username
    get_cliente_nombre.short_description = 'Cliente'

    def fecha_reserva_corta(self, obj):
        return obj.created_at.strftime('%d/%m/%Y')
    fecha_reserva_corta.short_description = 'Fecha'

    actions = ['confirmar_reservas', 'cancelar_reservas']

    def confirmar_reservas(self, request, queryset):
        updated = queryset.update(estado_reserva='CONFIRMADA')
        self.message_user(request, f"{updated} reservas confirmadas.")
    confirmar_reservas.short_description = 'Confirmar reservas seleccionadas'

    def cancelar_reservas(self, request, queryset):
        updated = queryset.update(estado_reserva='CANCELADA')
        self.message_user(request, f"{updated} reservas canceladas.")
    cancelar_reservas.short_description = 'Cancelar reservas seleccionadas'