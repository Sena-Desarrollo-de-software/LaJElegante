from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("lobby/", views.lobby, name="lobby"),
    path("habitaciones/", views.habitaciones, name="habitaciones"),
    path("restaurante/", views.restaurante, name="restaurante"),
    path("tyc/", views.tyc, name="tyc"),
    path("login/", views.LoginUsuario.as_view(), name="login"),
    path("signup/", views.signup, name="signup"),
    path("promociones/", views.promociones, name="promociones"),
]