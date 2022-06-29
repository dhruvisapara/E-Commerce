from category.fixtures import faker
from category.models import Category
import factory
from pdb import set_trace as pdb


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    categories = factory.LazyAttribute(lambda _: faker.categories())
    description = factory.LazyAttribute(lambda _: faker.description())
