import data_wizard
from .models import Impuesto, Tarifa, Temporada

data_wizard.register(Impuesto)
data_wizard.register(Tarifa)
data_wizard.register(Temporada)