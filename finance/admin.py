from django.contrib import admin
from django.utils import timezone
from django.urls import reverse
from django.utils.html import format_html
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET
from .models import Impuesto, Temporada, Tarifa, TarifaImpuesto

# === FUNCIONES AUXILIARES ===
def get_servicio_nombre(obj):
    if obj.servicio:
        return str(obj.servicio)
    return f"{obj.servicio_tipo} #{obj.servicio_id}"
get_servicio_nombre.short_description = 'Servicio'

def formatear_precio(precio):
    if not precio:
        return "Pendiente"
    return f"${precio:,.2f}".replace(',','.')

def get_precio_final_formateado(obj):
    return formatear_precio(obj.precio_final)
get_precio_final_formateado.short_description = 'Precio Final'

class TarifaImpuestoInline(admin.TabularInline):
    model = TarifaImpuesto
    extra = 1
    verbose_name = "impuesto aplicable"
    verbose_name_plural = "impuestos aplicables"
    
    fields = ('impuesto','is_active')
    autocomplete_fields = ['impuesto']


class TarifaInline(admin.TabularInline):
    model = Tarifa
    extra = 0
    fields = (
        get_servicio_nombre,
        'precio_base', 
        'estado', 
        get_precio_final_formateado
    )
    readonly_fields = (get_servicio_nombre,get_precio_final_formateado,)

@admin.register(Impuesto)
class ImpuestoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'get_tipo_display',
        'porcentaje',
        'get_aplica_a_display',
        'es_obligatorio',
        'aplica_extranjeros',
        'get_vigencia',
        'is_active'
    )
    
    list_filter = (
        'tipo',
        'aplica_a',
        'es_obligatorio',
        'aplica_extranjeros',
        'is_active',
        'fecha_vigencia_inicio',
        'fecha_vigencia_fin'
    )
    
    search_fields = ('nombre', 'texto_informativo')
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'tipo', 'porcentaje')
        }),
        ('Aplicación', {
            'fields': ('aplica_a', 'es_obligatorio', 'aplica_extranjeros')
        }),
        ('Vigencia', {
            'fields': ('fecha_vigencia_inicio', 'fecha_vigencia_fin')
        }),
        ('Información Adicional', {
            'fields': ('requiere_informacion_adicional', 'texto_informativo'),
            'classes': ('collapse',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    readonly_fields = AUDITORIA_READONLY
    
    def get_vigencia(self, obj):
        hoy = timezone.now().date()
        if obj.fecha_vigencia_fin and obj.fecha_vigencia_fin < hoy:
            return format_html('<span style="color: red;">{}</span>', '🔴 Expirado')
        elif obj.fecha_vigencia_inicio <= hoy:
            return format_html('<span style="color: green;">{}</span>', '🟢 Vigente')
        else:
            return format_html('<span style="color: orange;">{}</span>', '🟡 Próximo')
    get_vigencia.short_description = 'Estado vigencia'
    
    actions = ['duplicar_impuesto', 'marcar_expirado']
    
    def duplicar_impuesto(self, request, queryset):
        for impuesto in queryset:
            impuesto.pk = None
            impuesto.nombre = f"{impuesto.nombre} (copia)"
            impuesto.save()
        self.message_user(request, f"{queryset.count()} impuestos duplicados.")
    duplicar_impuesto.short_description = "Duplicar impuestos seleccionados"

@admin.register(Temporada)
class TemporadaAdmin(admin.ModelAdmin):
    list_display = (
        'get_nombre_display',
        'fecha_inicio',
        'fecha_fin',
        'porcentaje_modificador',
        'get_impacto',
        'total_tarifas',
        'is_active'
    )
    
    list_filter = (
        'nombre',
        'is_active',
        'fecha_inicio',
        'fecha_fin'
    )
    
    search_fields = ('nombre',)
    
    fieldsets = (
        ('Información de Temporada', {
            'fields': ('nombre', 'fecha_inicio', 'fecha_fin')
        }),
        ('Ajuste de Precios', {
            'fields': ('porcentaje_modificador',),
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    readonly_fields = AUDITORIA_READONLY + ('modificador_precio',)
    
    inlines = [TarifaInline]  # Muestra tarifas asociadas
    
    def get_impacto(self, obj):
        if obj.porcentaje_modificador > 0:
            return format_html('<span style="color: green;">⬆️ +{}%</span>', obj.porcentaje_modificador)
        elif obj.porcentaje_modificador < 0:
            return format_html('<span style="color: red;">⬇️ {}%</span>', obj.porcentaje_modificador)
        else:
            return format_html('<span style="color: gray;">➡️ 0%</span>')
    get_impacto.short_description = 'Impacto'
    
    def total_tarifas(self, obj):
        return obj.tarifas.count()
    total_tarifas.short_description = 'Tarifas'

@admin.register(Tarifa)
class TarifaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        get_servicio_nombre,
        'temporada',
        'precio_base',
        get_precio_final_formateado,
        'estado',
        'total_impuestos',
        'is_active'
    )
    
    list_filter = (
        'estado',
        'is_active',
        'temporada',
        'created_at'
    )
    
    search_fields = (
        'temporada__nombre',
    )
    
    fieldsets = (
        ('Configuración Básica', {
            'fields': ('servicio_tipo', 'servicio_id', 'temporada', 'estado')
        }),
        ('Precios', {
            'fields': ('precio_base', 'precio_final'),
            'description': 'El precio final se calcula automáticamente con impuestos'
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    readonly_fields = AUDITORIA_READONLY + (get_precio_final_formateado,)
    
    inlines = [TarifaImpuestoInline]

    raw_id_fields = ('servicio_tipo',)
    
    def total_impuestos(self, obj):
        count = obj.tarifaimpuesto_set.filter(is_active=True).count()
        return count
    total_impuestos.short_description = 'Impuestos'
    
    actions = ['calcular_precios', 'activar_tarifas', 'desactivar_tarifas']
    
    def calcular_precios(self, request, queryset):
        for tarifa in queryset:
            tarifa.save()
        self.message_user(request, f"{queryset.count()} tarifas recalculadas.")
    calcular_precios.short_description = "Recalcular precios finales"

@admin.register(TarifaImpuesto)
class TarifaImpuestoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tarifa', 'impuesto','is_active')
    list_filter = ('impuesto__tipo','is_active')
    search_fields = ('tarifa__tipo_habitacion__nombre_tipo', 'impuesto__nombre')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False  # Solo vista