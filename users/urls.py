from django.urls import path
from . import views

urlpatterns = [
    # === USUARIO ===
    path("usuario/", views.index_usuario, name="usuario_index"),
    path("usuario-create/", views.create_usuario, name="usuario_create"),
    path("usuario-update/<int:pk>/", views.update_usuario, name="usuario_update"),
    path("usuario-delete/<int:pk>", views.delete_usuario, name="usuario_delete"),
    path('usuario-trashcan/<int:pk>', views.trashcan_usuario, name='usuario_trashcan'),
    # === GRUPOS ===
    path("grupo/", views.index_grupo, name="grupo_index"),
    path("grupo-create/", views.create_grupo, name="grupo_create"),
    path("grupo-update/<int:pk>/", views.update_grupo, name="grupo_update"),
    path("grupo-delete/<int:pk>", views.delete_grupo, name="grupo_delete"),
    path('grupo-trashcan/<int:pk>', views.trashcan_grupo, name='grupo_trashcan'),
]