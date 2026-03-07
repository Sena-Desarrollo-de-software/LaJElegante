from django.db import models
from django.contrib.auth.models import AbstractUser,Group

#Se usaran los modelos de Django cada grupo = Rol
class Usuario(AbstractUser):
    # created_at = models.DateTimeField(auto_now_add=True) <- campo que esta en modelo User como data_joined
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # is_active = models.BooleanField(default=True) <- ya esta en modelo User bajo el mismo nombre

class GrupoProxy(Group):
    """Proxy para mostrar grupos en misma app que usuarios
    debido a que solo usa la tabla ya creada"""
    class Meta:
        proxy = True
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        app_label = 'users'