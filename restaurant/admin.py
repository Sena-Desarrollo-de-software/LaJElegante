from django.contrib import admin
from .models import Horario,Turno,ReservaRestaurante
from core.admin import AUDITORIA_READONLY, AUDITORIA_FIELDSET

@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    pass

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
    pass

@admin.register(ReservaRestaurante)
class ReservaRestauranteAdmin(admin.ModelAdmin):
    pass