from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task


# celery -A <mymodule> worker -l info -P eventlet
# notification.apply_async(eta=datetime.utcnow() + timedelta(seconds=1))
@shared_task
def notification():
    send_mail('Test',
              'text',
              settings.EMAIL_HOST_USER,
              ['isysbas@gmail.com'],
              html_message='<h1>{text}<h1>')
    return ''
