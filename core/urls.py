from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path("hotel/lobby/", views.lobby, name="lobby"),
    path("tyc/", TemplateView.as_view(template_name="hotel/tyc.html"), name="tyc"),
]