from django.urls import path
from . import views

urlpatterns = [
    path("hotel/lobby/", views.lobby, name="lobby"),
]
