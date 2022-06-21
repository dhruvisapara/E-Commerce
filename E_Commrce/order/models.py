from django.db import models
from django_extensions.db.models import ActivatorModel
from cart.models import Cart
from customer.models import Customer
from products.models import Products
from utils.constant import ORDER_STATUSES, SUBMITTED


class Order(ActivatorModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        default=None,
        related_name="cart_order",
        null=True,
    )
    product=models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    status = models.IntegerField(choices=ORDER_STATUSES, default=SUBMITTED)
    price = models.DecimalField(decimal_places=3, max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=50, default="", blank=True)
    address = models.CharField(max_length=50, default="", blank=True)

    # def save(self, *args, **kwargs):
    #     self.price = self.cart.get_total_cost
    #     super(Order, self).save(*args, **kwargs)


class Points(models.Model):
    order_point = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="order_points",
    )
    points_gained = models.IntegerField(default=0)
    user = models.OneToOneField(
        Customer, on_delete=models.CASCADE, default=None, related_name="user_point"
    )
