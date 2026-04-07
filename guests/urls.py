from django.urls import path
from . import views

app_name = 'guests'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('perfil/', views.perfil, name='perfil'),

    path('reservas/habitaciones/', views.reserva_habitacion_list, name='reserva_habitacion_list'),
    path('reservas/habitaciones/crear/', views.reserva_habitacion_create, name='reserva_habitacion_create'),
    path('reservas/habitaciones/<int:pk>/editar/', views.reserva_habitacion_update, name='reserva_habitacion_update'),
    path('reservas/habitaciones/<int:pk>/cancelar/', views.reserva_habitacion_cancel, name='reserva_habitacion_cancel'),
    path('reservas/<int:pk>/', views.reserva_detail, name='reserva_detail'),
    path('reservas/<int:pk>/editar/', views.reserva_edit, name='reserva_edit'),
    path('reservas/<int:pk>/cancelar/', views.reserva_cancel, name='reserva_cancel'),

    path('reservas/restaurante/', views.reserva_restaurante_list, name='reserva_restaurante_list'),
    path('reservas/restaurante/crear/', views.reserva_restaurante_create, name='reserva_restaurante_create'),
    path('reservas/restaurante/<int:pk>/editar/', views.reserva_restaurante_update, name='reserva_restaurante_update'),
    path('reservas/restaurante/<int:pk>/cancelar/', views.reserva_restaurante_cancel, name='reserva_restaurante_cancel'),

    path('tarifas/', views.tarifas_list, name='tarifas_list'),
    path('tipos-habitacion/', views.tipos_habitacion_list, name='tipos_habitacion_list'),
    path('horarios/', views.horarios_list, name='horarios_list'),
    path('turnos/', views.turnos_list, name='turnos_list'),
]
