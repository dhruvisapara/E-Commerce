import factory
from factory.django import DjangoModelFactory

from address.factories import AddressFactory
from cart.factories import CartFactory
from customer.factories import CustomerFactory
from order.models import Order


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    cart = factory.SubFactory(CartFactory)
    address= factory.SubFactory(AddressFactory)
    user = factory.SubFactory(CustomerFactory)
