from django.urls import path
from . import views

urlpatterns = [
    # === IMPUESTO ===
    path("impuesto/", views.index_impuesto, name="impuesto_index"),
    path("impuesto-create/", views.create_impuesto, name="impuesto_create"),
    path("impuesto-update/<int:pk>/", views.update_impuesto, name="impuesto_update"),
    path("impuesto-delete/<int:pk>", views.delete_impuesto, name="impuesto_delete"),
    path('impuesto-trashcan/<int:pk>', views.trashcan_impuesto, name='impuesto_trashcan'),
    # === TARIFA ===
    path("tarifa/", views.index_tarifa, name="tarifa_index"),
    path("tarifa-create/", views.create_tarifa, name="tarifa_create"),
    path("tarifa-update/<int:pk>/", views.update_tarifa, name="tarifa_update"),
    path("tarifa-delete/<int:pk>", views.delete_tarifa, name="tarifa_delete"),
    path('tarifa-trashcan/<int:pk>', views.trashcan_tarifa, name='tarifa_trashcan'),
    # === TEMPORADA ===
    path("temporada/", views.index_temporada, name="temporada_index"),
    path("temporada-create/", views.create_temporada, name="temporada_create"),
    path("temporada-update/<int:pk>/", views.update_temporada, name="temporada_update"),
    path("temporada-delete/<int:pk>", views.delete_temporada, name="temporada_delete"),
    path('temporada-trashcan/<int:pk>', views.trashcan_temporada, name='temporada_trashcan'),
]