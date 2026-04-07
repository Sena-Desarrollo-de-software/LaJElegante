from django.urls import path
from . import views

app_name = 'restaurant'

urlpatterns = [
    # === HORARIOS ===
    path('horario/', views.index_horario, name='horario_index'),
    path('horario-create/', views.create_horario, name='horario_create'),
    path('horario-update/<int:pk>/', views.update_horario, name='horario_update'),
    path('horario-delete/<int:pk>', views.delete_horario, name='horario_delete'),
    path('horario-trashcan/', views.trashcan_horario, name='horario_trashcan'),
    path('horario-restore/<int:pk>', views.restore_horario, name='horario_restore'),
    # === TURNOS ===
    path('turno/', views.index_turno, name='turno_index'),
    path('turno-create/', views.create_turno, name='turno_create'),
    path('turno-update/<int:pk>/', views.update_turno, name='turno_update'),
    path('turno-delete/<int:pk>', views.delete_turno, name='turno_delete'),
    path('turno-trashcan/', views.trashcan_turno, name='turno_trashcan'),
    path('turno-restore/<int:pk>', views.restore_turno, name='turno_restore'),
    path('turno-import/', views.import_turno, name='turno_import'),
    # === RESERVA RESTAURANTE ===
    path('reserva-restaurante/', views.index_reserva_restaurante, name='reserva_restaurante_index'),
    path('reserva-restaurante-create/', views.create_reserva_restaurante, name='reserva_restaurante_create'),
    path('reserva-restaurante-update/<int:pk>', views.update_reserva_restaurante, name='reserva_restaurante_update'),
    path('reserva-restaurante-delete/<int:pk>', views.delete_reserva_restaurante, name='reserva_restaurante_delete'),
    path('reserva-restaurante-trashcan/<int:pk>', views.trashcan_reserva_restaurante, name='reserva_restaurante_trashcan'),
]