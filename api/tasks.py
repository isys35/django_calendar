from django.conf import settings
from django.core.mail import send_mail
from api.management.commands import update_countries, update_holidays
from celery import shared_task


# celery -A <mymodule> worker -l info -P eventlet
from api.models import Country, Holiday, CountryHoliday


@shared_task
def notification(email: str, title: str, start_event: str, end_event: str):
    send_mail('Оповещение',
              'оповещение',
              settings.EMAIL_HOST_USER,
              [email],
              html_message=f'<h1>{title}</h1> C {start_event} по {end_event}')
    return True


@shared_task
def update_countries_holidays():
    update_countries.Command().handle()
    update_holidays.Command().handle()
