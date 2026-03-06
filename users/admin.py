from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from django.utils import timezone
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = (
        'id', 
        'username', 
        'email', 
        'first_name', 
        'last_name', 
        'is_active',
        'is_staff',
        'get_grupos',
        'date_joined',
        'updated_at'
    )
    
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    list_filter = (
        'is_active',
        'is_staff',           
        'is_superuser',
        'groups',
        'date_joined'
    )
    
    readonly_fields = ('date_joined', 'updated_at', 'last_login', 'deleted_at')
    
    # Organización del formulario
    fieldsets = (
        ('Información de Acceso', {
            'fields': ('username', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permisos y Roles', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'description': 'is_staff: Permite al usuario acceder al panel de administración',
            'classes': ('wide',),
        }),
        ('Fechas de Auditoría', {
            'fields': ('date_joined', 'last_login', 'updated_at', 'deleted_at'),
            'classes': ('collapse',),
        }),
    )
    
    # Campos para la creación de nuevos usuarios
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 
                'email', 
                'first_name', 
                'last_name', 
                'password1', 
                'password2', 
                'is_active',
                'is_staff',
                'groups'
            ),
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('groups')
    
    def get_grupos(self, obj):
        return ", ".join([group.name for group in obj.groups.all()]) if obj.groups.exists() else "Sin grupo"
    get_grupos.short_description = 'Grupos/Roles'
    
    # Acciones masivas para gestionar usuarios
    actions = ['activar_usuarios', 'desactivar_usuarios', 'marcar_como_eliminado']
    
    def activar_usuarios(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} usuarios activados.")
    activar_usuarios.short_description = "Activar usuarios seleccionados"
    
    def desactivar_usuarios(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} usuarios desactivados.")
    desactivar_usuarios.short_description = "Desactivar usuarios seleccionados"
    
    def marcar_como_eliminado(self, request, queryset):
        updated = queryset.update(deleted_at=timezone.now(), is_active=False)
        self.message_user(request, f"{updated} usuarios marcados como eliminados.")
    marcar_como_eliminado.short_description = "Marcar como eliminados (soft delete)"

class GrupoAdmin(GroupAdmin):
    list_display = ('id', 'name', 'user_count', 'lista_usuarios')
    search_fields = ('name',)
    filter_horizontal = ('permissions',)
    
    def user_count(self, obj):
        return obj.user_set.count()
    user_count.short_description = 'Total Usuarios'
    
    def lista_usuarios(self, obj):
        users = obj.user_set.all()[:5]
        user_list = [f"{user.username}" for user in users]
        if obj.user_set.count() > 5:
            user_list.append(f"... y {obj.user_set.count() - 5} más")
        return ", ".join(user_list) if user_list else "Sin usuarios"
    lista_usuarios.short_description = 'Usuarios en este grupo'
    
    fieldsets = (
        ('Información del Grupo', {
            'fields': ('name',)
        }),
        ('Permisos', {
            'fields': ('permissions',),
            'classes': ('wide',),
        }),
    )

admin.site.unregister(Group)
admin.site.register(Group, GrupoAdmin)

admin.site.site_header = 'Panel de Administración'
admin.site.site_title = 'Admin'
admin.site.index_title = 'Gestión de Usuarios y Roles'