from celery import app
from celery.utils.log import get_task_logger
from django.core.mail import send_mail
from E_Commrce.settings import EMAIL_HOST_USER
from order.models import Order

logger = get_task_logger(__name__)


@app.shared_task()
def order_conformation():

    user = Order.objects.all().last()
    mail_subject = " Order Confirmation"
    message = "Congratulations !!!! {} your order placed successfully.It's time for double  celebration you won ," \
              "congratulations you won {} points from this Order".format(
        user.user.username, user.points_gained
    )

    to_email = user.user.email
    send_mail(
        subject=mail_subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )

    return "done"
