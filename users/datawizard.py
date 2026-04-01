import data_wizard
from .models import Usuario, GrupoProxy

data_wizard.register(Usuario, options={
    'exclude': ['password', 'deleted_at'],
    'natural_keys': ['username'],
    'readonly': ['date_joined', 'updated_at'],
    # Esto permite importar grupos por su nombre
    'natural_foreign_keys': {
        'groups': 'users.GrupoProxy',  # Relación ManyToMany con grupos
    }
})

data_wizard.register(GrupoProxy, options={
    'exclude': ['permissions'],
    'natural_keys': ['name'],
})