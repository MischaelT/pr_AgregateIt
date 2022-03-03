from celery import shared_task

from django.core.mail import send_mail

from settings import settings


@shared_task
def activate_email(activation_link, email_to):
    """
    Celery task for email activation

    Args:
        activation_link (str): link for activation
        email_to (str): email for sending link
    """

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
