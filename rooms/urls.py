from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # === HABITACIÓN ===
    path("habitacion/", views.index_habitacion, name="habitacion_index"),
    path("habitacion-create/", views.create_habitacion, name="habitacion_create"),
    path("habitacion-update/<int:pk>/", views.update_habitacion, name="habitacion_update"),
    path("habitacion-delete/<int:pk>", views.delete_habitacion, name="habitacion_delete"),
    path("habitacion-trashcan/", views.trashcan_habitacion, name="habitacion_trashcan"),
    path("habitacion-restore/<int:pk>", views.restore_habitacion, name="habitacion_restore"),
    path('habitacion-import/', views.import_habitacion, name='habitacion_import'),
    path('habitacion-frame/', views.descargar_plantilla_habitaciones, name='habitacion_frame'),
    path('habitacion-process/', views.procesar_import_habitacion, name='habitacion_process'),
    # === RESERVA HABITACIÓN ===
    path("reserva-habitacion/", views.index_reserva_habitacion, name="reserva_habitacion_index"),
    path("reserva-habitacion-create/<int:reserva_id>/", views.create_reserva_habitacion, name="reserva_habitacion_create"),
    path("reserva-habitacion-update/<int:pk>/", views.update_reserva_habitacion, name="reserva_habitacion_update"),
    path("reserva-habitacion-cancel/<int:pk>/", views.cancel_reserva_habitacion, name="reserva_habitacion_cancel"),
    # === TIPO HABITACIÓN
    path("tipo-habitacion/", views.index_tipo_habitacion, name="tipo_habitacion_index"),
    path("tipo-habitacion-create/", views.create_tipo_habitacion, name="tipo_habitacion_create"),
    path("tipo-habitacion-update/<int:pk>/", views.update_tipo_habitacion, name="tipo_habitacion_update"),
    path("tipo-habitacion-delete/<int:pk>", views.delete_tipo_habitacion, name="tipo_habitacion_delete"),
    path("tipo-habitacion-trashcan/", views.trashcan_tipo_habitacion, name="tipo_habitacion_trashcan"),
    path("tipo-habitacion-restore/<int:pk>", views.restore_tipo_habitacion, name="tipo_habitacion_restore"),
]
