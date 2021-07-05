from django.contrib.auth.models import AbstractUser
from django.db import models

from api.manager import UserManager


class MyUser(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []
    objects = UserManager()
