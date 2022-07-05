from random import random

import factory
from factory.django import DjangoModelFactory

from category.factories import CategoryFactory
from customer.factories import CustomerFactory
from products.models import Products


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Products

    name = factory.Faker("name")
    price = factory.Faker('pyint', min_value=0, max_value=1000)
    brand = factory.Faker("name")
    new_price = factory.Faker('pyint', min_value=0, max_value=1000)
    old_price = factory.Faker('pyint', min_value=0, max_value=1000)
    quantity = factory.Faker("random_number")
    user = factory.SubFactory(CustomerFactory)
    is_bestseller = factory.Faker('pybool')
    is_featured = factory.Faker('pybool')
    created_at = factory.Faker('date')
    updated_at = factory.Faker('date')

    # category = factory.SubFactory(CategoryFactory)
