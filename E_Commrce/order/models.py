from django.db import models
from django_extensions.db.models import ActivatorModel
from cart.models import CartItem
from customer.models import Customer
from products.models import Products


class Order(ActivatorModel):
    product = models.ForeignKey(Products, on_delete=models.CASCADE, default=None)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE, default=None)
    cart = models.ForeignKey(CartItem, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(decimal_places=3, max_digits=10)
    date_added = models.DateTimeField(auto_now_add=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    address = models.CharField(max_length=50, default='', blank=True)

    # to save the data
    def placeOrder(self):
        self.save()

    # This method is for filter order by customer id
    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
