from celery import shared_task

from django.core.mail import send_mail

from settings import settings

@shared_task
def activate_email(activation_link, email_to):
    subject = 'Activate your account'
    body = f'''
    Hello!
    Please refer to link to activate your account
    {activation_link}
    '''
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST,
        [email_to],
        fail_silently=False,
    )
