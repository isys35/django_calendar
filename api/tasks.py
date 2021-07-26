from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from api.models import UserEvent


# celery -A <mymodule> worker -l info -P eventlet
# notification.apply_async(eta=datetime.utcnow() + timedelta(seconds=1))
@shared_task
def notification(event: UserEvent):
    send_mail('Оповещение',
              'оповещение',
              settings.EMAIL_HOST_USER,
              [event.user.email],
              html_message=f'<h1>{event.title}</h1> C {event.start_event} по {event.end_event}')
    return True
