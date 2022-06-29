from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from E_Commrce.settings import EMAIL_HOST_USER
from order.models import Points

logger = get_task_logger(__name__)


@shared_task()
def order_conformation():
    user_order = Points.objects.all().last()
    mail_subject = " Order Confirmation"

    message = (
        "Congratulations !!!! {} your order placed successfully.It time for double celebration"
        "you won {} points."
        .format(
            user_order.user.username, user_order.points_gained
        )
    )
    to_email = user_order.user.email

    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=False,
    )

    return "done"
