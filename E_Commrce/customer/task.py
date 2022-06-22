from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from E_Commrce.settings import EMAIL_HOST_USER
from customer.models import Customer, Business

logger = get_task_logger(__name__)


@shared_task()
def send_email_task():
    user = Customer.objects.filter().last()
    mail_subject = " Registration Conformation"
    message = (
        "Hello {} Thank you for registering now you are in our community."
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


@shared_task()
def mail_about_business_for_admin():
    business_user = Business.objects.filter().last()
    mail_subject = " New Business Registration"
    message = (
        "Hello Admin ,This mail regarding new business registration Please check the company details./"
        "Company Name-{},"
        "Company Revenue - {} , "
        "Company contact person name-{} , "
        "Company email -{} ".format(
            business_user.company_name,
            business_user.revenue,
            business_user.business_customer.username,
            business_user.business_customer.email,
        )
    )
    to_email = EMAIL_HOST_USER

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=business_user.business_customer.email,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "done"
