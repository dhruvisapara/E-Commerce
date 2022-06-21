from django.db.models.signals import post_save
from django.dispatch import receiver
from customer.models import Business


@receiver(post_save, sender=Business)
def buisness_user(sender, instance, *args, **kwargs):
    instance.business_customer.is_staff = True
    # instance.save()
