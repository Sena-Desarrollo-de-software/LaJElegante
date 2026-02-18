from django.db import models
from django.contrib.auth.models import AbstractUser

#Se usaran los modelos de Django cada grupo = Rol
class Usuario(AbstractUser):
    # created_at = models.DateTimeField(auto_now_add=True) <- campo que esta en modelo User como data_joined
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    # is_active = models.BooleanField(default=True) <- ya esta en modelo User bajo el mismo nombre