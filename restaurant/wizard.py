import data_wizard
from .models import ReservaRestaurante, Turno, Horario

data_wizard.register(ReservaRestaurante)
data_wizard.register(Turno)
data_wizard.register(Horario)