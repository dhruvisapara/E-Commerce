import random

from factory.django import DjangoModelFactory
import factory

from customer.models import Customer
from utils.constant import GENDER


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    username = factory.Faker("name")
    password = 'setpassword1234'
    birth_date = factory.Faker("date")
    gender = random.choice([x[1] for x in GENDER])
    address = factory.Faker("name")
    age = factory.Faker("random_number")
    phone_number = factory.Faker("random_number")
    is_staff = True
    is_superuser = True
