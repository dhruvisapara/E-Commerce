from django.db import models
from django_extensions.db.models import ActivatorModel
from rest_framework.exceptions import ValidationError

from E_Commrce.settings import AUTH_USER_MODEL
from address.models import Address
from cart.models import Cart
from products.models import Products
from utils.constant import ORDER_STATUSES, SUBMITTED


class Order(ActivatorModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.SET_NULL,
        default=None,
        related_name="cart_order",
        null=True,
        blank=True,
    )
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)
    tax = models.IntegerField(default=0)
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        related_name="order_address",
        null=True,
        blank=True,
        default=None,
    )
    estimated_delivery_charges = models.IntegerField(default=0)
    total_cost = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        if self.cart.get_total_cost <= 2000:
            self.estimated_delivery_charges = 99
        self.price = self.cart.get_total_cost
        return super(Order, self).save(*args, **kwargs)


class Points(models.Model):
    order_point = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="order_points",
    )
    points_gained = models.IntegerField(default=0)
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=None,
        related_name="user_point",
    )
