from django.urls import path
from . import views

app_name = "rooms"

urlpatterns = [
    path("", views.habitacion_list, name="habitacion_list"),
    path("crear/", views.habitacion_create, name="habitacion_create"),
    path("editar/<int:pk>/", views.habitacion_update, name="habitacion_update"),
    path("eliminar/<int:pk>/", views.habitacion_delete, name="habitacion_delete"),
]
