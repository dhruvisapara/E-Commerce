from decimal import Decimal
from django.db import models
from customer.models import Customer
from products.models import Products
from django_extensions.db.models import ActivatorModel


class Cart(ActivatorModel):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    number_of_items = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)
    text_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)
    text_percentage = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)

    # def __str__(self):
    #     return str(self.id)


class CartItem(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, default=None, related_name="items"
    )
    quantity = models.PositiveIntegerField()
    cart_item = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        default=None,
        null=True,
        blank=True,
        related_name="carts",
    )

    def get_total_price(self):
        return self.product.price * self.quantity


    # def get_cart_deal_total(self):
    #     orderitem = self.cart_item.number_of_items()
    #     total = sum(item.get_total_price for item in orderitem)
    #     return total
