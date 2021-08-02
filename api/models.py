from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta

from api.managers import UserManager


class Country(models.Model):
    name = models.CharField(max_length=40, db_index=True, unique=True, primary_key=True)


class Holiday(models.Model):
    name = models.CharField(max_length=200, db_index=True, unique=True, primary_key=True)
    countries = models.ManyToManyField(Country, related_name='holidays', through="CountryHoliday")


class CountryHoliday(models.Model):
    class Meta:
        unique_together = ("country", "holiday", "date")

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )
    holiday = models.ForeignKey(
        Holiday,
        on_delete=models.CASCADE,
    )
    date = models.DateTimeField()


class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL,
                                verbose_name='Страна',
                                related_name='users', default=None, null=True, blank=True)

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
