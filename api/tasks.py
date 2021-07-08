from django.core.mail import send_mail

from celery import shared_task

# notification.apply_async(eta=datetime.utcnow() + timedelta(seconds=1))
@shared_task
def notification():
    send_mail('Test',
              'text',
              'isys35@mail.ru',
              ['isys46@mail.ru'],
              html_message='<h1>{text}<h1>')