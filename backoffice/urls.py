from django.urls import path
from . import views

app_name = 'backoffice'

urlpatterns = [
    path('dashboard/' ,views.dashboard, name='dashboard'),
    path('reserva-create/' ,views.create_reserva, name='reserva_create'),
    path('reserva-detail/<int:pk>' ,views.detail_reserva, name='reserva_detail'),
    path('reserva/' ,views.index_reserva, name='reserva_index')
]