from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart
from order.models import Order


@receiver(post_save, sender=Cart)
def cart_order_generated(sender, instance, *args, **kwargs):
    print("called")
    Order.objects.create(cart=instance, user_id=instance.user.id)
