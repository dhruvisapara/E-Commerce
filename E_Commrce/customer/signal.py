from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Business, Customer
from customer.task import send_email_task, mail_about_business_for_admin


@receiver(post_save, sender=Business)
def business_user(sender, instance, *args, **kwargs):
    business_user = instance.business_customer
    business_user.is_staff = True
    mail_about_business_for_admin.delay()
    business_user.save()


@receiver(post_save, sender=Customer)
def mail_sent_after_sign_up(sender, instance, *args, **kwargs):
    send_email_task.delay()
