from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('dashboard/' ,views.dashboard, name='dashboard'),
    path('reserva/' ,views.create_reserva, name='reserva_create'),
    path('reserva/' ,views.index_reserva, name='reserva_index')
]