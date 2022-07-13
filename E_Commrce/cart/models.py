from django.db import models
from E_Commrce.settings import AUTH_USER_MODEL
from products.models import Products
from django_extensions.db.models import ActivatorModel


class Cart(ActivatorModel):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, default=None)
    number_of_items = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)
    text_total = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)
    text_percentage = models.DecimalField(default=0.00, max_digits=5, decimal_places=3)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_cost(self):
        total_cost = sum(item.get_total_price() for item in self.carts.all())
        return total_cost

    @property
    def get_total_items(self):
        total_item = sum(item.get_quantity() for item in self.carts.all())
        return total_item

    def save(self, *args, **kwargs):
        instance = super(Cart, self).save(*args, **kwargs)
        self.total = self.get_total_cost
        self.number_of_items = self.get_total_items
        return instance


class CartItem(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, null=True, related_name="items"
    )
    quantity = models.PositiveIntegerField()
    cart_item = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="carts",
    )

    def get_total_price(self):
        return self.product.price * self.quantity

    def get_quantity(self):
        return self.quantity
