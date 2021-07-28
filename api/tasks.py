from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


# celery -A <mymodule> worker -l info -P eventlet

@shared_task
def notification(email: str, title: str, start_event: str, end_event: str):
    send_mail('Оповещение',
              'оповещение',
              settings.EMAIL_HOST_USER,
              [email],
              html_message=f'<h1>{title}</h1> C {start_event} по {end_event}')
    return True
