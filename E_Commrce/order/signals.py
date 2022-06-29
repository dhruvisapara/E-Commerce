from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from order.models import Order, Points
from order.tasks import order_conformation
from utils.constant import PROCESSED
from pdb import set_trace as pdb


@receiver(pre_save, sender=Order)
def pre_save_order(sender, instance, *args, **kwargs):
    """
        After creating Order make status 0 for that order
    """
    instance.status = 0


@receiver(post_save, sender=Order)
def post_save_order(sender, instance, *args, **kwargs):
    """
        After creating order it should generate points for that order.
        make status processed for that order.
        calculate tax and final amount for order.
    """
    Points.objects.create(order_point=instance, user_id=instance.user.id)
    instance.status = PROCESSED
    order_tax = int(instance.price) * 0.01
    instance.tax = order_tax
    instance.total_cost = int(instance.tax) + int(instance.price) + int(instance.estimated_delivery_charges)


@receiver(post_save, sender=Order)
def update_points(sender, instance, created, **kwargs):
    """
        It should generate points for total_cost and add points in existing points if user
        already have.

    """
    if created:

        if instance.price <= 3000:

            points_gained = 0.03 * int(instance.price)
            instance.points_gained = points_gained

        else:
            points_gained = 0.02 * int(instance.price)
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
    """
        It should call after order creation and sent mail to order user.
        This mail consists order total amount and points that this order generated.
    """
    order_conformation.delay()
