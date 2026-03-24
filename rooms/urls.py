from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # === HABITACIÓN ===
    path("habitacion/", views.index_habitacion, name="habitacion_index"),
    path("habitacion-create/", views.create_habitacion, name="habitacion_create"),
    path("habitacion-update/<int:pk>/", views.update_habitacion, name="habitacion_update"),
    path("habitacion-delete/<int:pk>", views.delete_habitacion, name="habitacion_delete"),
    path('habitacion-trashcan/<int:pk>', views.trashcan_habitacion, name='habitacion_trashcan'),
    # === RESERVA HABITACIÓN ===
    path("reserva-restaurante/", views.index_reserva_restaurante, name="reserva_restaurante_index"),
    path("reserva-restaurante-create/", views.create_reserva_restaurante, name="reserva_restaurante_create"),
    path("reserva-restaurante-update/<int:pk>/", views.update_reserva_restaurante, name="reserva_restaurante_update"),
    path("reserva-restaurante-delete/<int:pk>", views.delete_reserva_restaurante, name="reserva_restaurante_delete"),
    path('reserva-restaurante-trashcan/<int:pk>', views.trashcan_reserva_restaurante, name='reserva_restaurante_trashcan'),
    # === TIPO HABITACIÓN
    path("tipo-habitacion/", views.index_tipo_habitacion, name="tipo_habitacion_index"),
    path("tipo-habitacion-create/", views.create_tipo_habitacion, name="tipo_habitacion_create"),
    path("tipo-habitacion-update/<int:pk>/", views.update_tipo_habitacion, name="tipo_habitacion_update"),
    path("tipo-habitacion-delete/<int:pk>", views.delete_tipo_habitacion, name="tipo_habitacion_delete"),
    path('tipo-habitacion-trashcan/<int:pk>', views.trashcan_tipo_habitacion, name='tipo_habitacion_trashcan'),
]
