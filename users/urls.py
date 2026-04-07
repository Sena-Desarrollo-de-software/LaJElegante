from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # === USUARIO ===
    path('usuario/', views.index_usuario, name='usuario_index'),
    path('usuario-create/', views.create_usuario, name='usuario_create'),
    path('usuario-update/<int:pk>/', views.update_usuario, name='usuario_update'),
    path('usuario-delete/<int:pk>/', views.delete_usuario, name='usuario_delete'),
    path('usuario-trashcan/', views.trashcan_usuario, name='usuario_trashcan'),
    path('usuario-restore/<int:pk>/', views.restore_usuario, name='usuario_restore'),
    path('usuario-import/', views.import_usuario, name='usuario_import'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    # === GRUPOS ===
    path('grupo/', views.index_grupo, name='grupo_index'),
    path('grupo-create/', views.create_grupo, name='grupo_create'),
    path('grupo-update/<int:pk>/', views.update_grupo, name='grupo_update'),
    path('grupo-delete/<int:pk>/', views.delete_grupo, name='grupo_delete'),
    path('grupo-trashcan/', views.trashcan_grupo, name='grupo_trashcan'),
    path('grupo-restore/<int:pk>/', views.restore_grupo, name='grupo_restore'),
    path('grupo-import/', views.import_grupo, name='grupo_import'),
    # === PERFIL ===
    path("perfil-update/<int:pk>", views.update_usuario_auto, name="profile_update"),
    path("perfil-update-email/", views.send_password_reset_email, name="profile_update_email")
]