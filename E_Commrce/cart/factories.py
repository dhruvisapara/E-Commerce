from decimal import Decimal

import factory
from factory.django import DjangoModelFactory
from faker.generator import random

from cart.models import Cart, CartItem
from customer.factories import CustomerFactory
from products.factories import ProductFactory


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(CustomerFactory)
    number_of_items = factory.Faker("random_number")
    total = factory.LazyFunction(lambda: Decimal(1.21))
    text_total = factory.LazyFunction(lambda: Decimal(1.21))
    text_percentage = factory.LazyFunction(lambda: Decimal(1.21))


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker('random_number')
    cart_item = factory.SubFactory(CartFactory)

