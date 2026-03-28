from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from core.constants import SERVICIOS_TARIFABLES
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET
from .models import Impuesto, Temporada, Tarifa, TarifaImpuesto
from .forms import TarifaAdminForm

# === FUNCIONES AUXILIARES ===
def get_servicio_nombre(obj):
    if not obj.servicio_tipo_id or not obj.servicio_id:
        return "Sin servicio"
    
    try:
        ct = obj.servicio_tipo
        print(f"ContentType: {ct}")
        key = (ct.app_label, ct.model)
        print(f"Key: {key}")
        
        if key in SERVICIOS_TARIFABLES:
            info = SERVICIOS_TARIFABLES[key]
            from django.apps import apps
            model = apps.get_model(ct.app_label, info['model'])
            servicio = model.objects.get(id=obj.servicio_id)
            return f"{info['emoji']} {servicio} ({info['nombre']})"
        else:
            return f"📄 {ct} #{obj.servicio_id}"
            
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {ct} #{obj.servicio_id}"

def formatear_precio(precio):
    if not precio:
        return "Pendiente"
    return f"${precio:,.2f}".replace(',', '.')

def get_precio_final_formateado(obj):
    return formatear_precio(obj.precio_final)
get_precio_final_formateado.short_description = 'Precio Final'

class TarifaImpuestoInline(admin.TabularInline):
    model = TarifaImpuesto
    extra = 1
    verbose_name = "impuesto aplicable"
    verbose_name_plural = "impuestos aplicables"
    
    fields = ('impuesto', 'is_active')
    autocomplete_fields = ['impuesto']


class TarifaInline(admin.TabularInline):
    model = Tarifa
    extra = 0
    fields = (
        'get_servicio_nombre_inline',
        'precio_base', 
        'estado', 
        get_precio_final_formateado
    )
    readonly_fields = ('get_servicio_nombre_inline', get_precio_final_formateado,)
    
    def get_servicio_nombre_inline(self, obj):
        return get_servicio_nombre(obj)
    get_servicio_nombre_inline.short_description = 'Servicio'


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
    
    actions = ['duplicar_impuesto']
    
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
    
    readonly_fields = AUDITORIA_READONLY
    
    inlines = [TarifaInline]
    
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
    form = TarifaAdminForm

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
        'servicio_id',
    )
    
    fieldsets = (
        ('Configuración Básica', {
            'fields': ('servicio_selector', 'temporada', 'estado')
        }),
        ('Precios', {
            'fields': ('precio_base',),
            'description': 'El precio final se calcula automáticamente con impuestos'
        }),
        ('Estados', {
            'fields': ('is_active',)
        }),
        AUDITORIA_FIELDSET,
    )
    
    readonly_fields = AUDITORIA_READONLY + (get_precio_final_formateado, 'precio_final')
    
    inlines = [TarifaImpuestoInline]
    
    def total_impuestos(self, obj):
        return obj.tarifaimpuesto_set.filter(is_active=True).count()
    total_impuestos.short_description = 'Impuestos'
    
    actions = ['calcular_precios', 'activar_tarifas', 'desactivar_tarifas']
    
    def calcular_precios(self, request, queryset):
        for tarifa in queryset:
            tarifa.save()
        self.message_user(request, f"{queryset.count()} tarifas recalculadas.")
    calcular_precios.short_description = "Recalcular precios finales"
    
    def activar_tarifas(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} tarifas activadas.")
    activar_tarifas.short_description = "Activar tarifas seleccionadas"
    
    def desactivar_tarifas(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} tarifas desactivadas.")
    desactivar_tarifas.short_description = "Desactivar tarifas seleccionadas"


@admin.register(TarifaImpuesto)
class TarifaImpuestoAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_tarifa_servicio', 'impuesto', 'is_active')
    list_filter = ('impuesto__tipo', 'is_active')
    search_fields = ('tarifa__servicio_id', 'impuesto__nombre')
    
    def get_tarifa_servicio(self, obj):
        return get_servicio_nombre(obj.tarifa)
    get_tarifa_servicio.short_description = 'Servicio'
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False