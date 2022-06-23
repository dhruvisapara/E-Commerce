from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from cart.models import Cart, CartItem
from order.models import Order


# @receiver(post_save, sender=Cart)
# def cart_order_generated(sender, instance, *args, **kwargs):
#     print("called")
#     Order.objects.create(cart=instance, user_id=instance.user.id)


@receiver(post_save, sender=CartItem)
def update_product_quantity(sender, instance, created, **kwargs):
    if created:

        product_quantity = instance.product
        product_quantity.quantity = F("quantity") - 1
        product_quantity.save()
