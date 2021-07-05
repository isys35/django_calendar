from django.contrib.auth.models import AbstractUser
from django.db import models

from api.managers import UserManager


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserEvent(models.Model):
    NOTIFICATIONS = [
        ('1HOUR', 'За час'),
        ('2HOUR', 'За два часа'),
        ('4HOUR', 'За 4 часа'),
        ('DAY', 'За день'),
        ('WEEK', 'За неделю'),
    ]
    title = models.CharField(max_length=40, verbose_name='Событие', db_index=True)
    start_event = models.DateTimeField()
    end_event = models.DateTimeField()
    notification = models.CharField(max_length=30,
                                    choices=NOTIFICATIONS,
                                    db_index=True,
                                    verbose_name='Напоминание',
                                    blank=True,
                                    null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='events')
