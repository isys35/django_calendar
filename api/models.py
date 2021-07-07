from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

from api.managers import UserManager


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()


class UserEvent(models.Model):
    NOTIFICATIONS = [
        (timedelta(hours=1), 'За час'),
        (timedelta(hours=2), 'За два часа'),
        (timedelta(hours=4), 'За 4 часа'),
        (timedelta(days=3), 'За день'),
        (timedelta(weeks=1), 'За неделю'),
    ]
    title = models.CharField(max_length=40, verbose_name='Событие', db_index=True)
    start_event = models.DateTimeField()
    end_event = models.DateTimeField()
    notification = models.DurationField(max_length=30,
                                        choices=NOTIFICATIONS,
                                        db_index=True,
                                        verbose_name='Напоминание',
                                        blank=True,
                                        null=True)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='events')
