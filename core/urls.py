from django.urls import path
from . import views

urlpatterns = [
    path("lobby/", views.lobby, name="lobby"),
    path("habitaciones/", views.habitaciones, name="habitaciones"),
    path("restaurante/", views.restaurante, name="restaurante"),
    path("login/", views.login, name="login"),
    path("signup/", views.signup, name="signup"),
    path("tyc/", views.tyc, name="tyc"),
]
