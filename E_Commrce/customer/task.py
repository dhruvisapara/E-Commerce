from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from E_Commrce.settings import EMAIL_HOST_USER
from customer.models import Customer

logger = get_task_logger(__name__)


@shared_task()
def send_email_task():
    user = Customer.objects.all().last()
    mail_subject = " Registration Conformation"
    message = (
        "Hello {} Thank you for visiting our site"
        " Your username  - {} and password  -{} ".format(user.username, user.password)
    )
    to_email = user.email

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "done"
