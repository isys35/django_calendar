from django.contrib.auth.models import AbstractUser
from django.db import models

from api.managers import UserManager


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()