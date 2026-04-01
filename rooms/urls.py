from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # === HABITACIÓN ===
    path("habitacion/", views.index_habitacion, name="habitacion_index"),
    path("habitacion-create/", views.create_habitacion, name="habitacion_create"),
    path("habitacion-update/<int:pk>/", views.update_habitacion, name="habitacion_update"),
    path("habitacion-delete/<int:pk>", views.delete_habitacion, name="habitacion_delete"),
    path("habitacion/trashcan/", views.trashcan_habitacion, name="habitacion_trashcan"),
    path("habitacion/<int:pk>/restore/", views.restore_habitacion, name="habitacion_restore"),
    # === RESERVA HABITACIÓN ===
    path("reserva-habitacion/", views.index_reserva_habitacion, name="reserva_habitacion_index"),
    path("reserva-habitacion-create/", views.create_reserva_habitacion, name="reserva_habitacion_create"),
    path("reserva-habitacion-update/<int:pk>/", views.update_reserva_habitacion, name="reserva_habitacion_update"),
    path("reserva-habitacion-delete/<int:pk>", views.delete_reserva_habitacion, name="reserva_habitacion_delete"),
    path('reserva-habitacion-trashcan/<int:pk>', views.trashcan_reserva_habitacion, name='reserva_habitacion_trashcan'),
    # === TIPO HABITACIÓN
    path("tipo-habitacion/", views.index_tipo_habitacion, name="tipo_habitacion_index"),
    path("tipo-habitacion-create/", views.create_tipo_habitacion, name="tipo_habitacion_create"),
    path("tipo-habitacion-update/<int:pk>/", views.update_tipo_habitacion, name="tipo_habitacion_update"),
    path("tipo-habitacion-delete/<int:pk>", views.delete_tipo_habitacion, name="tipo_habitacion_delete"),
    path('tipo-habitacion-trashcan/<int:pk>', views.trashcan_tipo_habitacion, name='tipo_habitacion_trashcan'),
]
