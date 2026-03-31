# users/migrations/0002_create_groups_and_permissions.py
from django.db import migrations

def crear_grupos_y_permisos(apps, schema_editor):
    """
    Crea los 6 grupos y asigna permisos según especificaciones.
    Incluye grupo Clientes con permisos de solo lectura limitados.
    """
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    
    # ========== 1. PERMISOS POR APP ==========
    
    # App Finance
    finance_models = ['tarifa', 'impuesto', 'temporada']
    finance_perms_full = []
    finance_perms_view_only = []
    finance_perms_no_delete = []
    
    for model in finance_models:
        # Full CRUD (incluye delete) - solo Administrador
        finance_perms_full.extend([
            f'add_{model}', f'change_{model}', 
            f'delete_{model}', f'view_{model}'
        ])
        # Solo lectura
        finance_perms_view_only.append(f'view_{model}')
        # Todo excepto delete (para Asistente y Gerente General)
        finance_perms_no_delete.extend([
            f'add_{model}', f'change_{model}', f'view_{model}'
        ])
    
    # App Restaurant
    restaurant_models = ['horario', 'turno', 'reservarestaurante']
    restaurant_perms_full = []
    restaurant_perms_no_delete = []
    restaurant_perms_view_only = []  # Para clientes
    
    for model in restaurant_models:
        restaurant_perms_full.extend([
            f'add_{model}', f'change_{model}', 
            f'delete_{model}', f'view_{model}'
        ])
        restaurant_perms_no_delete.extend([
            f'add_{model}', f'change_{model}', f'view_{model}'
        ])
        restaurant_perms_view_only.append(f'view_{model}')
    
    # App Rooms
    rooms_models = ['tipohabitacion', 'habitacion', 'reservahabitacion']
    rooms_perms_full = []
    rooms_perms_no_delete = []
    rooms_perms_view_only = []  # Para clientes
    
    for model in rooms_models:
        rooms_perms_full.extend([
            f'add_{model}', f'change_{model}', 
            f'delete_{model}', f'view_{model}'
        ])
        rooms_perms_no_delete.extend([
            f'add_{model}', f'change_{model}', f'view_{model}'
        ])
        rooms_perms_view_only.append(f'view_{model}')
    
    # App Users
    users_models = ['usuario', 'group']
    users_perms_full = []
    users_perms_no_delete = []
    users_perms_view_only = []  # Clientes NO ven usuarios
    
    for model in users_models:
        users_perms_full.extend([
            f'add_{model}', f'change_{model}', 
            f'delete_{model}', f'view_{model}'
        ])
        users_perms_no_delete.extend([
            f'add_{model}', f'change_{model}', f'view_{model}'
        ])
        # Clientes NO tienen permisos de users
    
    # App Core (modelo Reserva)
    core_models = ['reserva']
    core_perms_full = []
    core_perms_view_only = []
    core_perms_no_delete = []
    core_perms_self_only = []  # Para clientes (ver solo sus reservas)
    
    for model in core_models:
        core_perms_full.extend([
            f'add_{model}', f'change_{model}', 
            f'delete_{model}', f'view_{model}'
        ])
        core_perms_view_only.append(f'view_{model}')
        core_perms_no_delete.extend([
            f'add_{model}', f'change_{model}', f'view_{model}'
        ])
        # Clientes: pueden ver sus reservas (filtrado por queryset) y crear nuevas
        core_perms_self_only.extend([
            f'add_{model}', f'view_{model}'  # Puede crear y ver, pero NO change/delete
        ])
    
    # ========== 2. CONFIGURACIÓN DE GRUPOS ==========
    
    grupos_config = {
        'Administrador': {
            'permisos': (
                finance_perms_full + restaurant_perms_full + 
                rooms_perms_full + users_perms_full + core_perms_full
            )
        },
        'Gerente General': {
            'permisos': (
                finance_perms_no_delete + restaurant_perms_no_delete + 
                rooms_perms_no_delete + core_perms_no_delete
            )
        },
        'Gerente de Habitaciones': {
            'permisos': (
                finance_perms_view_only + rooms_perms_no_delete + 
                core_perms_no_delete
            )
        },
        'Gerente de Comidas y Bebidas': {
            'permisos': (
                finance_perms_view_only + restaurant_perms_no_delete + 
                core_perms_no_delete
            )
        },
        'Asistente Administrativo': {
            'permisos': (
                finance_perms_no_delete + restaurant_perms_no_delete + 
                rooms_perms_no_delete + core_perms_no_delete
            )
        },
        'Clientes': {
            'permisos': (
                finance_perms_view_only +           # Ver tarifas, impuestos, temporadas
                restaurant_perms_view_only +        # Ver horarios, turnos (solo lectura)
                rooms_perms_view_only +             # Ver tipos de hab, habitaciones
                core_perms_self_only                # Crear y ver SUS reservas
            ),
            # NOTA: Los clientes NO tienen permisos sobre users
            # El filtrado por usuario se hará en las vistas/querysets
        }
    }
    
    # ========== 3. OBTENER PERMISOS EXISTENTES ==========
    
    all_permission_codenames = set()
    for config in grupos_config.values():
        all_permission_codenames.update(config['permisos'])
    
    # Obtener solo los permisos que existen
    existing_permissions = Permission.objects.filter(
        codename__in=all_permission_codenames
    )
    perm_dict = {p.codename: p for p in existing_permissions}
    
    # Reportar permisos faltantes (no detiene la migración)
    missing_perms = all_permission_codenames - set(perm_dict.keys())
    if missing_perms:
        print("\n⚠️  ATENCIÓN: Permisos NO encontrados (esto puede ser normal si las apps no han migrado):")
        for perm in sorted(missing_perms):
            print(f"   - {perm}")
        print("\n   Los grupos se crearán igualmente, pero sin estos permisos.")
        print("   Cuando las otras apps migren, ejecuta: python manage.py migrate users again\n")
    
    # ========== 4. CREAR GRUPOS Y ASIGNAR PERMISOS ==========
    
    for group_name, config in grupos_config.items():
        group, created = Group.objects.get_or_create(name=group_name)
        
        status = "✓ CREADO" if created else "→ EXISTE"
        print(f"{status} Grupo: {group_name}")
        
        # Asignar solo los permisos que existen
        permisos_asignar = [perm_dict[cd] for cd in config['permisos'] if cd in perm_dict]
        group.permissions.set(permisos_asignar)
        
        if len(permisos_asignar) == len(config['permisos']):
            print(f"  └→ ✅ {len(permisos_asignar)}/{len(config['permisos'])} permisos asignados")
        else:
            print(f"  └→ ⚠️  {len(permisos_asignar)}/{len(config['permisos'])} permisos asignados ({len(config['permisos']) - len(permisos_asignar)} faltantes)")


def eliminar_grupos(apps, schema_editor):
    """Rollback: elimina los 6 grupos"""
    Group = apps.get_model('auth', 'Group')
    nombres = [
        'Administrador', 'Gerente General', 'Gerente de Habitaciones',
        'Gerente de Comidas y Bebidas', 'Asistente Administrativo', 'Clientes'
    ]
    count = Group.objects.filter(name__in=nombres).delete()[0]
    if count:
        print(f"✓ Rollback: {count} grupos eliminados")


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
        ('core', '__first__'),
        ('finance', '__first__'),
        ('restaurant', '__first__'),
        ('rooms', '__first__'),
    ]
    
    operations = [
        migrations.RunPython(crear_grupos_y_permisos, eliminar_grupos),
    ]