# users/migrations/0003_create_test_users.py
from django.db import migrations
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist


def crear_usuarios_prueba(apps, schema_editor):
    """
    Crea usuarios de prueba organizados por grupos
    Incluye 10 clientes adicionales para pruebas
    """

    Group = apps.get_model('auth', 'Group')
    Usuario = apps.get_model('users', 'Usuario')

    PASSWORD = 'Prueba123!'  # ⚠️ Cambiar en producción

    # ========= 1. VALIDAR GRUPOS =========
    grupos_nombres = [
        'Administrador',
        'Gerente General',
        'Gerente de Habitaciones',
        'Gerente de Comidas y Bebidas',
        'Asistente Administrativo',
        'Clientes'  # Nuevo grupo
    ]

    grupos = {}

    for nombre in grupos_nombres:
        try:
            grupos[nombre] = Group.objects.get(name=nombre)
            print(f"✓ Grupo encontrado: {nombre}")
        except Group.DoesNotExist:
            raise ObjectDoesNotExist(
                f"El grupo '{nombre}' no existe. Ejecuta primero la migración 0002."
            )

    # ========= 2. DEFINICIÓN DE USUARIOS =========
    usuarios_data = {
        'Administrador': [
            {
                'username': 'admin_principal',
                'email': 'admin@lajelegante.com',
                'first_name': 'Admin',
                'last_name': 'Principal'
            },
            {
                'username': 'admin_backup',
                'email': 'admin2@lajelegante.com',
                'first_name': 'Admin',
                'last_name': 'Backup'
            },
            {
                'username': 'admin_seguridad',
                'email': 'admin3@lajelegante.com',
                'first_name': 'Admin',
                'last_name': 'Seguridad'
            },
            {
                'username': 'jeremy_duarte',
                'email': 'jeremydamian.db@gmail.com',
                'first_name': 'Jeremy',
                'last_name': 'Duarte'
            }
        ],
        'Gerente General': [
            {
                'username': 'gerente_general_1',
                'email': 'gerente1@lajelegante.com',
                'first_name': 'Carlos',
                'last_name': 'López'
            },
            {
                'username': 'gerente_general_2',
                'email': 'gerente2@lajelegante.com',
                'first_name': 'María',
                'last_name': 'García'
            },
            {
                'username': 'gerente_general_3',
                'email': 'gerente3@lajelegante.com',
                'first_name': 'Juan',
                'last_name': 'Rodríguez'
            }
        ],
        'Gerente de Habitaciones': [
            {
                'username': 'gerente_hab_1',
                'email': 'ghabitaciones1@lajelegante.com',
                'first_name': 'Ana',
                'last_name': 'Martínez'
            },
            {
                'username': 'gerente_hab_2',
                'email': 'ghabitaciones2@lajelegante.com',
                'first_name': 'Luis',
                'last_name': 'Sánchez'
            },
            {
                'username': 'gerente_hab_3',
                'email': 'ghabitaciones3@lajelegante.com',
                'first_name': 'Carmen',
                'last_name': 'Pérez'
            }
        ],
        'Gerente de Comidas y Bebidas': [
            {
                'username': 'gerente_cyb_1',
                'email': 'gcomidas1@lajelegante.com',
                'first_name': 'Roberto',
                'last_name': 'Gómez'
            },
            {
                'username': 'gerente_cyb_2',
                'email': 'gcomidas2@lajelegante.com',
                'first_name': 'Sofía',
                'last_name': 'Fernández'
            },
            {
                'username': 'gerente_cyb_3',
                'email': 'gcomidas3@lajelegante.com',
                'first_name': 'Diego',
                'last_name': 'Torres'
            }
        ],
        'Asistente Administrativo': [
            {
                'username': 'asistente_1',
                'email': 'asistente1@lajelegante.com',
                'first_name': 'Laura',
                'last_name': 'Ramírez'
            },
            {
                'username': 'asistente_2',
                'email': 'asistente2@lajelegante.com',
                'first_name': 'Pedro',
                'last_name': 'Castro'
            },
            {
                'username': 'asistente_3',
                'email': 'asistente3@lajelegante.com',
                'first_name': 'Elena',
                'last_name': 'Morales'
            }
        ],
        'Clientes': [
            {
                'username': 'cliente_juan',
                'email': 'juan.perez@email.com',
                'first_name': 'Juan',
                'last_name': 'Pérez'
            },
            {
                'username': 'cliente_maria',
                'email': 'maria.gonzalez@email.com',
                'first_name': 'María',
                'last_name': 'González'
            },
            {
                'username': 'cliente_carlos',
                'email': 'carlos.rodriguez@email.com',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez'
            },
            {
                'username': 'cliente_ana',
                'email': 'ana.fernandez@email.com',
                'first_name': 'Ana',
                'last_name': 'Fernández'
            },
            {
                'username': 'cliente_luis',
                'email': 'luis.martinez@email.com',
                'first_name': 'Luis',
                'last_name': 'Martínez'
            },
            {
                'username': 'cliente_laura',
                'email': 'laura.sanchez@email.com',
                'first_name': 'Laura',
                'last_name': 'Sánchez'
            },
            {
                'username': 'cliente_diego',
                'email': 'diego.torres@email.com',
                'first_name': 'Diego',
                'last_name': 'Torres'
            },
            {
                'username': 'cliente_carmen',
                'email': 'carmen.diaz@email.com',
                'first_name': 'Carmen',
                'last_name': 'Díaz'
            },
            {
                'username': 'cliente_javier',
                'email': 'javier.moreno@email.com',
                'first_name': 'Javier',
                'last_name': 'Moreno'
            },
            {
                'username': 'cliente_isabel',
                'email': 'isabel.romero@email.com',
                'first_name': 'Isabel',
                'last_name': 'Romero'
            }
        ]
    }

    # ========= 3. CREAR USUARIOS =========
    total_creados = 0
    total_actualizados = 0
    
    print("\n" + "="*60)
    print("🚀 CREANDO USUARIOS DE PRUEBA")
    print("="*60)
    
    for grupo_nombre, usuarios_lista in usuarios_data.items():
        grupo = grupos[grupo_nombre]
        print(f"\n📋 Grupo: {grupo_nombre} ({len(usuarios_lista)} usuarios)")
        
        for user_data in usuarios_lista:
            usuario, created = Usuario.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'password': make_password(PASSWORD),
                    'is_active': True,
                    'is_staff': grupo_nombre == 'Administrador',
                    'is_superuser': user_data['username'] == 'admin_principal',
                }
            )
            
            if created:
                total_creados += 1
                print(f"  ✓ CREADO: {user_data['username']} ({user_data['first_name']} {user_data['last_name']})")
            else:
                total_actualizados += 1
                print(f"  → ACTUALIZADO: {user_data['username']}")
                # Actualizar datos por si acaso
                usuario.email = user_data['email']
                usuario.first_name = user_data['first_name']
                usuario.last_name = user_data['last_name']
                usuario.password = make_password(PASSWORD)
            
            # ✅ Asignar SOLO el grupo correcto
            usuario.groups.set([grupo])
            
            # ✅ Configuración especial para admins
            if grupo_nombre == 'Administrador':
                usuario.is_staff = True
                if user_data['username'] == 'admin_principal':
                    usuario.is_superuser = True
            
            # ✅ Configuración especial Jeremy
            if user_data['username'] == 'jeremy_duarte':
                usuario.is_staff = True
                usuario.is_superuser = True
            
            # ✅ Clientes NUNCA son staff
            if grupo_nombre == 'Clientes':
                usuario.is_staff = False
                usuario.is_superuser = False
            
            usuario.save()
    
    # ========= 4. RESUMEN FINAL =========
    print("\n" + "="*60)
    print("📊 RESUMEN DE CREACIÓN")
    print("="*60)
    print(f"✅ Usuarios nuevos creados: {total_creados}")
    print(f"🔄 Usuarios actualizados: {total_actualizados}")
    print(f"👥 Total usuarios en sistema: {Usuario.objects.count()}")
    print(f"\n🔑 Contraseña para todos: {PASSWORD}")
    print("="*60)
    
    # Mostrar resumen por grupo
    print("\n📋 USUARIOS POR GRUPO:")
    for grupo_nombre, grupo_obj in grupos.items():
        usuarios_grupo = grupo_obj.user_set.all()
        print(f"\n  📌 {grupo_nombre}: {usuarios_grupo.count()} usuarios")
        for user in usuarios_grupo[:5]:  # Mostrar primeros 5
            staff_marker = "⭐" if user.is_staff else "  "
            super_marker = "👑" if user.is_superuser else "  "
            print(f"     {staff_marker}{super_marker} {user.username} - {user.email}")
        if usuarios_grupo.count() > 5:
            print(f"     ... y {usuarios_grupo.count() - 5} más")


def eliminar_usuarios_prueba(apps, schema_editor):
    """
    Rollback: elimina los usuarios de prueba creados
    """
    Usuario = apps.get_model('users', 'Usuario')

    usuarios_a_eliminar = [
        # Administradores
        'admin_principal', 'admin_backup', 'admin_seguridad', 'jeremy_duarte',
        # Gerentes Generales
        'gerente_general_1', 'gerente_general_2', 'gerente_general_3',
        # Gerentes de Habitaciones
        'gerente_hab_1', 'gerente_hab_2', 'gerente_hab_3',
        # Gerentes de Comidas y Bebidas
        'gerente_cyb_1', 'gerente_cyb_2', 'gerente_cyb_3',
        # Asistentes
        'asistente_1', 'asistente_2', 'asistente_3',
        # Clientes (10)
        'cliente_juan', 'cliente_maria', 'cliente_carlos', 'cliente_ana',
        'cliente_luis', 'cliente_laura', 'cliente_diego', 'cliente_carmen',
        'cliente_javier', 'cliente_isabel'
    ]

    deleted_count = Usuario.objects.filter(username__in=usuarios_a_eliminar).delete()[0]
    print(f"✓ Rollback: {deleted_count} usuarios eliminados")


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_create_groups_and_permissions'),
    ]

    operations = [
        migrations.RunPython(crear_usuarios_prueba, eliminar_usuarios_prueba),
    ]