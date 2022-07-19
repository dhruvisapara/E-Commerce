import factory
from factory.django import DjangoModelFactory

from address.models import Address
from customer.factories import CustomerFactory


class AddressFactory(DjangoModelFactory):
    class Meta:
        model = Address

    user_address = factory.SubFactory(CustomerFactory)
    email = "dhruvi.sapara@trootech.com"
    phone = factory.Faker('random_number')
    name = factory.Faker('name')
    building_name = factory.Faker('name')
    block = factory.Faker('name')
    floor = factory.Faker('name')
    flat_number = factory.Faker('name')
    street = factory.Faker('name')
    area = factory.Faker('name')
