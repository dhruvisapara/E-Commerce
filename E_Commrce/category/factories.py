from factory.django import DjangoModelFactory
from category.models import Category
import factory
from customer.factories import CustomerFactory


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    categories = factory.Faker("name")
    description = factory.Faker("name")
    user = factory.SubFactory(CustomerFactory)


class SubCaegoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    categories = factory.Faker("name")
    description = factory.Faker("name")
    user = factory.SubFactory(CustomerFactory)
