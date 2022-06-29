from django.db.models.signals import post_save
from django.dispatch import receiver

from customer.models import Business, Customer
from customer.tasks import send_email_task, mail_about_business_for_admin
from pdb import set_trace as pdb


@receiver(post_save, sender=Business)
def business_user(sender, instance, *args, **kwargs):
    """
        After Business created current user staff status will be activated.
        And nail sent to admin.
        That mail contains registered business details.
    """
    business_user = instance.business_customer
    business_user.is_staff = True
    mail_about_business_for_admin.delay()
    business_user.save()


@receiver(post_save, sender=Customer)
def mail_sent_after_sign_up(sender, instance, *args, **kwargs):
    """
        When User  registered their self then confirmation mail is sent.
    """
    send_email_task.delay()
