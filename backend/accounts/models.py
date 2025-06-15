# models.py
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    pass  # Tu peux ajouter des champs ici plus tard (comme téléphone, etc.)
