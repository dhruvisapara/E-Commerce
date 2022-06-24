from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from order.models import Order, Points
from order.task import order_conformation
from utils.constant import PROCESSED


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, *args, **kwargs):
    instance.status = 0


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, *args, **kwargs):
    # import pdb;pdb.set_trace()
    Points.objects.create(order_point=instance, user_id=instance.user.id)
    instance.status = PROCESSED
    order_tax = int(instance.price) * 0.01
    instance.tax = order_tax
    instance.total_cost = int(instance.tax) + int(instance.price) + int(instance.estimated_delivery_charges)


@receiver(post_save, sender=Order)
def update_points(sender, instance, created, **kwargs):
    if created:

        if instance.price <= 10000:

            points_gained = 0.01 * int(instance.price)
            instance.points_gained = points_gained

        else:
            points_gained = 0.75 * int(instance.price)
            instance.points_gained = points_gained

        try:
            # Check if user already has points and update if so

            points = Points.objects.get(user=instance.user)
            points.points_gained = points_gained
            points.save(update_fields=["points_gained"])

        except Points.DoesNotExist:
            # User does not have points yet, create points
            Points.objects.create(user=instance.user, points_gained=points_gained)


@receiver(post_save, sender=Points)
def order_confirmation_mail(sender, instance, *args, **kwargs):
    order_conformation.delay()
