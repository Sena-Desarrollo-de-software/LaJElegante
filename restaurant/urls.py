from django.urls import path
from . import views

urlpatterns = [
    # === HORARIOS ===
    path('horario/', views.index_horario, name='horario_index'),
    path('horario-create/', views.create_horario, name='horario_create'),
    path('horario-update/<int:pk>', views.update_horario, name='horario_update'),
    path('horario-delete/<int:pk>', views.delete_horario, name='horario_delete'),
    path('horario-trashcan/<int:pk>', views.trashcan_horario, name='horario_trashcan'),
    # === MESAS ===
    path('mesa/', views.index_mesa, name='mesa_index'),
    path('mesa-create/', views.create_mesa, name='mesa_create'),
    path('mesa-update/<int:pk>', views.update_mesa, name='mesa_update'),
    path('mesa-delete/<int:pk>', views.delete_mesa, name='mesa_delete'),
    path('mesa-trashcan/<int:pk>', views.trashcan_mesa, name='mesa_trashcan'),
    # === RESERVA RESTAURANTE ===
    path('reserva-restaurante/', views.index_reserva_restaurante, name='reserva_restaurante_index'),
    path('reserva-restaurante-create/', views.create_reserva_restaurante, name='reserva_restaurante_create'),
    path('reserva-restaurante-update/<int:pk>', views.update_reserva_restaurante, name='reserva_restaurante_update'),
    path('reserva-restaurante-delete/<int:pk>', views.delete_reserva_restaurante, name='reserva_restaurante_delete'),
    path('reserva-restaurante-trashcan/<int:pk>', views.trashcan_reserva_restaurante, name='reserva_restaurante_trashcan'),
]